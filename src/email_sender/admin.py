from django.contrib import admin
from email_sender.models import Contact, MessageTemplate, ContactGroup



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "owner",
    )
    search_fields = (
        "name",
        "email",
    )
    list_filter = ("owner",)

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "created_at",
    )
    search_fields = (
        "title",
        "subject",
    )
    list_filter = ( "created_at",)




@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "created_at",
    )
    search_fields = ("title",)
    filter_horizontal = ("contacts",)#для админки.2 колонки для вкл в список