from django.contrib import admin
from .models import Notice, Answer


# Register your models here.
class NoticeAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Notice, NoticeAdmin)
admin.site.register(Answer)