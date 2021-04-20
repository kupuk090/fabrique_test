from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model

from .models import Poll, Question, AnswerGateway
from .permissions import PollPermission, QuestionPermission, AnswerGatewayPermission
from .serializers import PollSerializer, QuestionSerializer, AnswerGatewaySerializer


USER_MODEL = get_user_model()


class PollViewSet(viewsets.ModelViewSet):
    """
    REST API for polls.
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (PollPermission, )


class QuestionViewSet(viewsets.ModelViewSet):
    """
    REST API for questions.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (QuestionPermission, )


class AnswerGatewayViewSet(viewsets.ModelViewSet):
    """
    REST API for user's answer
    """
    queryset = AnswerGateway.objects.all()
    serializer_class = AnswerGatewaySerializer
    permission_classes = (AnswerGatewayPermission, )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ("user", )

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            return serializer.save(user=user)
        else:
            
            return serializer.save(user=USER_MODEL.objects.create(username=f"AnonymousUser{USER_MODEL.objects.last().id}"))

        return super().perform_create(serializer)
