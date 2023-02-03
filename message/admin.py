from django.contrib import admin
from .models import Message
# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'msg_sender', 'msg_receiver', 'seen']
    search_fields = ['msg_sender', 'msg_receiver']
    list_filter=['msg_sender', 'msg_receiver', 'seen']


admin.site.register(Message, MessageAdmin)