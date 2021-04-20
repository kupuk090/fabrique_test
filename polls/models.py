from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


USER_MODEL = get_user_model()


class Poll(models.Model):
    title = models.CharField(_("Poll title"), max_length=1024)
    created = models.DateTimeField(_("Poll created datetime"), auto_now=False, auto_now_add=True)
    start_date = models.DateField(_("Poll start date"), auto_now=False, auto_now_add=False)
    finish_date = models.DateField(_("Poll finish date"), auto_now=False, auto_now_add=False)
    description = models.CharField(_("Poll description"), max_length=8192)

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")

    def __str__(self):
        return self.title


class Question(models.Model):
    TEXT = "T"
    ONE_CHOICE = "C"
    MULTIPAL_CHOICES = "M"
    ANSWERS_TYPE_CHOICES = [
        (TEXT, "Text"),
        (ONE_CHOICE, "One choice"),
        (MULTIPAL_CHOICES, "Multipal choices")
    ]

    text = models.CharField(_("Question text"), max_length=4096)
    type = models.CharField(_("Question type"), choices=ANSWERS_TYPE_CHOICES, default=TEXT, max_length=1)
    poll = models.ForeignKey("Poll", related_name="questions", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_type_valid",
                check=models.Q(type__in=("T", "C", "M")),
            )
        ]

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey("Question", related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(_("Choice text"), max_length=4096)
 
    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    def __str__(self):
        return self.text


class AnswerGateway(models.Model):
    poll = models.ForeignKey("Poll", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField(_("User's answers created datetime"), auto_now=False, auto_now_add=True)


class Answer(models.Model):
    answer_gateway = models.ForeignKey("AnswerGateway", related_name="answers", on_delete=models.DO_NOTHING)
    question = models.ForeignKey("Question", on_delete=models.DO_NOTHING)
    choices = models.ManyToManyField("Choice", blank=True, null=True)
    value = models.CharField(_("User's answer text"), max_length=4096, blank=True, null=True)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
