from django.contrib.auth import get_user_model
from rest_framework import serializers

from datetime import date

from .models import Poll, Question, Choice, AnswerGateway, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "text", )
        read_only_fields = ("id", )


class QuestionSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Question.ANSWERS_TYPE_CHOICES, required=True)
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ("id", "type", "text", "choices", "poll")
        read_only_fields = ("id", )
        extra_kwargs = {
            "poll": {"write_only": True}
        }

    def validate(self, data):
        if data["type"] == Question.TEXT:
            if data.get("choices"):
                raise serializers.ValidationError({"choices": f"Choices not allowed for {data['type']} type of question"})
        else:
            if len(data["choices"]) < 2:
                raise serializers.ValidationError({"choices": f"Question must contain minimun 2 choices for {data['type']} type of question"})

        return super().validate(data)

    def create(self, validated_data):
        choices = validated_data.pop("choices", [])
        question = Question.objects.create(**validated_data)
        Choice.objects.bulk_create([Choice(question=question, **choice) for choice in choices])

        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop("choices", [])
        instance.choices.all().delete()
        Choice.objects.bulk_create([Choice(question=instance, **choice) for choice in choices])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = ("id", "title", "description", "start_date", "finish_date", "questions", )
        read_only_fields = ("id", )
        extra_kwargs = {
            "start_date": {"required": True}
        }

    def validate(self, data):
        if data["finish_date"]:
            if data["finish_date"] < data["start_date"]:
                raise serializers.ValidationError({"finish_date": "Finish date must be after start date"})

        return super().validate(data)

    def update(self, instance, validated_data):
        validated_data.pop("start_date")
        super().update(instance, validated_data)

        return instance


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False, required=False)
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), write_only=True, many=False)
    choices = ChoiceSerializer(many=True, required=False)
    choice_ids = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all(), write_only=True, many=True, required=False)

    class Meta:
        model = Answer
        fields = ("id", "question_id", "question", "choice_ids", "choices", "value", )
        read_only_fields = ("id", "question", "choices")

    def validate(self, data):
        if data["question_id"].type == Question.TEXT:
            if not data.get("value"):
                raise serializers.ValidationError({"value": f"This field is required for {data['question_id'].type} type of question"})
        else:
            if not data.get("choice_ids"):
                raise serializers.ValidationError({"choice_ids": f"This field is required for {data['question_id'].type} type of question"})
            
            question_choices = data["question_id"].choices.all()
            for choice in data["choice_ids"]:
                if choice not in question_choices:
                    raise serializers.ValidationError({"choice_ids": f"Choice with id={choice.id} does not belong to the question with id={data['question_id'].id}"})
 
            if (data["question_id"].type == Question.ONE_CHOICE) and (len(data["choice_ids"]) != 1):
                raise serializers.ValidationError({"choice_ids": f"This field should contain only 1 choice for {data['question_id'].type} type of question"})
            elif (data["question_id"].type == Question.MULTIPAL_CHOICES) and (len(data["choice_ids"]) < 1):
                raise serializers.ValidationError({"choice_ids": f"This field should contain minimum 1 choice for {data['question_id'].type} type of question"})

        
        return super().validate(data)



class AnswerGatewaySerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)
    poll = PollSerializer(many=False, required=False)
    today = date.today()
    poll_id = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.filter(start_date__lte=today, finish_date__gte=today), write_only=True)

    class Meta:
        model = AnswerGateway
        fields = ("id", "poll_id", "poll", "user", "created", "answers", )
        read_only_fields = ("id", "user", "created", "poll", )

    def create(self, validated_data):
        answers = validated_data.pop("answers", [])
        answer_gateway = AnswerGateway.objects.create(poll=validated_data.pop("poll_id"), **validated_data)
        
        for answer in answers:
            question = answer.pop("question_id")
            choices = answer.pop("choice_ids", [])
            a = Answer(answer_gateway=answer_gateway, question=question, **answer)
            a.save()
            for choice in choices:
                a.choices.add(choice)

        return answer_gateway
