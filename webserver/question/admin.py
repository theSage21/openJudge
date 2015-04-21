from django.contrib import admin
from question import models

admin.site.register(models.Profile)
admin.site.register(models.Language)
admin.site.register(models.Attempt)
admin.site.register(models.Question)
admin.site.register(models.AnswerType)
admin.site.register(models.Answer)
