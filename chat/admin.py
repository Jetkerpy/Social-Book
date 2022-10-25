from django.contrib import admin
from .models import ChatOnetoOne


# Register your models here.


class ChatAdmin(admin.ModelAdmin):
        list_display = ['sender', 'receiver', 'body', 'time']



admin.site.register(ChatOnetoOne, ChatAdmin)