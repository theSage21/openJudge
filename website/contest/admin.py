from django.contrib import admin
from contest import models

class TestCaseInlineAdmin(admin.TabularInline):
    model = models.TestCase


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Contest)
class ContestAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [TestCaseInlineAdmin]


@admin.register(models.TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Attempt)
class AttemptAdmin(admin.ModelAdmin):
    pass
