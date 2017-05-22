from django.contrib import admin
from contests import models


class TestCaseInlineAdmin(admin.TabularInline):
    model = models.TestCase

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'link')

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [TestCaseInlineAdmin]
    list_display = ('title', 'contest')

@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'contest', 'nick')

@admin.register(models.Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('language', 'question', 'participant', 'assessed', 'valid', 'submission_time')
