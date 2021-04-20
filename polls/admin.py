from django.contrib import admin

from .models import Poll, Question, Choice, Answer, AnswerGateway


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(AnswerGateway)
