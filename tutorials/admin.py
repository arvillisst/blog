from django.contrib import admin
from .models import Category, Tutorial, IpUser

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'created' )
    list_filter = ['category']
    date_hierarchy = 'created'



admin.site.register(IpUser)