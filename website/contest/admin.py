from django.contrib import admin
from contest import models

class TestCaseInlineAdmin(admin.TabularInline):
    model = models.TestCase


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contest', 'allowed')


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'live', 'published')


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [TestCaseInlineAdmin]
    list_display = ('title', 'contest')


@admin.register(models.TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('question', 'profile', 'language', 'correct')
    list_order=('question', 'profile', 'language', 'correct')
