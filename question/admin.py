from django.contrib import admin
from question import models
from django.utils import timezone
class AttemptAdmin(admin.ModelAdmin):
    list_filter=['correct','question','player']
    list_display=['pk','question','player','language','correct','not_checked']
    def not_checked(self,obj):
        return (timezone.now()-obj.stamp).__str__()
    not_checked.short_description='Time since submission'
    not_checked.allow_tags=True

admin.site.register(models.Player)
admin.site.register(models.Question)
admin.site.register(models.Attempt,AttemptAdmin)
admin.site.register(models.Language)
