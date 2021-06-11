from django.contrib import admin

# Register your models here.
from home.models import CompanyInformation, ContactMessage, FAQ


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'update_at', 'status']
    readonly_fields = ('name', 'email', 'message', 'ip')
    list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'ordernumber', 'status', 'update_at', 'create_at']
    list_filter = ['status']



admin.site.register(CompanyInformation, SettingAdmin)  # добавляет в админку Категории
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)
