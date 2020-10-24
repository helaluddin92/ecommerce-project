from django.contrib import admin
from .models import Setting, ContactMessage
# Register your models here.


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'keyword', 'phone',
                    'email', 'description', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'created_at']


admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
