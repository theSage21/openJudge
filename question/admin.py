from django.contrib import admin
from question import models
admin.site.register(models.Player)
admin.site.register(models.Question)
admin.site.register(models.Attempt)
admin.site.register(models.Language)
