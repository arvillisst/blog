from django.db.models import Count
from django.views.generic.base import ContextMixin
from .models import Category, Article, Comment
from taggit.models import Tag
from tutorials.models import Category as CategoryTutorial
from .forms import SearchForm, SubscriberForm
from newsletters.forms import NewsLetterUserSignUpForm
from newsletters.models import NewsletterUser
from django.contrib.contenttypes.models import ContentType


class CategoryMixin(ContextMixin):

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['category_from_mixin'] = Category.objects.all()[:2]
        context['category_tutorials'] = CategoryTutorial.objects.all()

        pop_articles = Article.objects.order_by('-hit_count_generic__hits')[:5]
        context['popular_articles'] = pop_articles.select_related('category')

        """ Сортировка по кол-ву комментариев 5, 4, 3, 2, 1 """
        order_by_comments = Article.objects.annotate(num_comments=Count('comments')).order_by('-num_comments').select_related('category')

        """ Сортировка по кол-ву комментариев, и по дате добавления комментариев (новые в начале) """
        context['order_by_comments'] = order_by_comments.annotate(comments_by_created=Count('comments__created'))[:5]
        
        order_by_commentes = Comment.objects.all()#.order_by('-num_comments').select_related('category')
        context['order_by_commentes'] = order_by_commentes
        

        context['all_tags'] = Tag.objects.all()
        context['search_form'] = SearchForm()
        context['form_subscr'] = SubscriberForm()
        context['form_newsletter'] = NewsLetterUserSignUpForm()

        context['newsletter_users'] = NewsletterUser.objects.all()
        return context