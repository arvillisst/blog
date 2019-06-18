from django.contrib import admin
from .models import Category, Article, IpUser, Comment, Subscriber
from django.core.mail import send_mass_mail
from config import settings
from django.urls import reverse

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    list_display = ('category', 'title', 'created')
    list_display_links = ('title',)
    list_select_related = ('category',)
    search_fields = ('title', 'content')
    list_filter = ['category']
    date_hierarchy = 'created'
    list_per_page = 15

    actions = ['email_customers']

    def email_customers(self, request, queryset):
        for subscriber in Subscriber.objects.all():
            for article in queryset:
                s = "На сайте 'Django - блог' появилась новость: \n\n" + article.title + "\n\nhttp://localhost:8000" + reverse('article_detail', kwargs={'category': article.category.slug, 'slug': article.slug})
                letters = []
                email_body = """ Здравствуйте {}. На сайте вышла новая статья статья {}.""".format(subscriber.email, article.title)
                letters = letters + [("Уведомление с сайта Django - блог", "Здpавствуйте " + "\n\n" + s, settings.DEFAULT_FROM_EMAIL, [subscriber.email])]
                send_mass_mail(letters, fail_silently=True)
                
    email_customers.short_description = 'Рассылка новости подписчикам'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'object_id', 'created')
    # list_filter = ['category']
    # date_hierarchy = 'created'


admin.site.register(IpUser)
admin.site.register(Subscriber)
