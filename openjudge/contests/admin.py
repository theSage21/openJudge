from django.contrib import admin
from contests import models


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Contest)
class ContestAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Attempt)
class AttemptAdmin(admin.ModelAdmin):
    pass
