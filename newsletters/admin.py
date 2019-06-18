from django.contrib import admin
from .models import NewsletterUser


@admin.register(NewsletterUser)
class NewsLettersAdmin(admin.ModelAdmin):
    list_display = ('email', 'created')



