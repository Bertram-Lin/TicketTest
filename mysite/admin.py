from django.contrib import admin
from mysite import models

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'message', 'enabled', 'pub_time')
    ordering = ('-pub_time',)

admin.site.register(models.Mood)
admin.site.register(models.Post)
admin.site.register(models.PermissionRole)
admin.site.register(models.login)
admin.site.register(models.Severitys)
admin.site.register(models.Prioritys)
admin.site.register(models.ticket)