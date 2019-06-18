from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, redirect
import csv
from .models import Category, Article, IpUser, Subscriber
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import wget
from taggit.models import Tag
from django.views.generic import ListView, View, CreateView
from .mixins import CategoryMixin
from hitcount.views import HitCountDetailView
from .forms import CommentForm, SearchForm, SubscriberForm, ContactForm
from newsletters.models import NewsletterUser
import json
import simplejson
from tutorials.models import Tutorial
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.mail import send_mail
from config import settings
from django.conf import settings


class HomeView(ListView, CategoryMixin):
    ''' Главная страница'''
    template_name = 'blog/home2.html'
    model = Article

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        # context['categorie'] = self.model.objects.get()
        context['articles'] = self.model.objects.all().order_by('-created')[:6]

        # pagination
        cats_list = self.model.objects.all().order_by('-created')
        cats_list = cats_list.select_related('category')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(cats_list, 6)
        try:
            context['cats'] = paginator.page(page)
        except PageNotAnInteger:
            context['cats'] = paginator.page(1)
        except EmptyPage:
            context['cats'] = paginator.page(paginator.num_pages)
        return context


class CategoryDetailView(CategoryMixin, HitCountDetailView):
    ''' Статьи конкретной категории'''
    template_name = 'blog/category.html'
    model = Category
    # count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['articles_by_category'] = self.get_object().article_set.all()
        context['category'] = self.get_object()

        # pagination
        cats_list = self.get_object().article_set.all().order_by('-created')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(cats_list, 6)
        try:
            context['cats'] = paginator.page(page)
        except PageNotAnInteger:
            context['cats'] = paginator.page(1)
        except EmptyPage:
            context['cats'] = paginator.page(paginator.num_pages)
        return context


class ArticleDetailView(HitCountDetailView, CategoryMixin):
    ''' Страница с детальной информацией'''
    template_name = 'blog/single-blog.html'
    model = Article
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context['categories'] = self.model.objects.all().select_related('category')
        context['article'] = self.get_object()
        context['form'] = CommentForm()
        context['article_comments'] = self.get_object().comments.all().order_by('-created')

        # # похожие статьи
        # article_tags_ids = self.get_object().tags.values_list('id', flat=True)
        # similar_articles = self.model.objects.filter(tags__in=article_tags_ids).exclude(id=self.get_object().id)
        # similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
        # context['similar_articles'] = similar_articles

        # следующая и предыдущая статьи
        context['prev_post'] = self.get_object().category.article_set.filter(id__lt=self.object.id).order_by('id').reverse().first()
        context['next_post'] = self.get_object().category.article_set.filter(id__gt=self.object.id).order_by('id').first()
        return context


class TagIndexView(CategoryMixin, ListView):
    template_name = 'blog/tags.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(TagIndexView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['object_list'] = self.model.objects.filter(tags__slug=self.kwargs.get('slug')).order_by('-created')

        object_list = self.model.objects.filter(tags__slug=self.kwargs.get('slug')).order_by('-created')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(object_list, 6)
        try:
            context['cats'] = paginator.page(page)
        except PageNotAnInteger:
            context['cats'] = paginator.page(1)
        except EmptyPage:
            context['cats'] = paginator.page(paginator.num_pages)
        return context


class SearchArticleView(ListView, CategoryMixin):
    model = Article
    template_name = 'blog/search.html'
    form = SearchForm()
    query = None

    def get_context_data(self, *args, **kwargs):
        context = super(SearchArticleView, self).get_context_data(*args, **kwargs)
        if 'query' in self.request.GET:
            self.form = SearchForm(self.request.GET)
            if self.form.is_valid():
                self.query = self.form.cleaned_data['query']
                context['results_count'] = self.model.objects.select_related('category').filter(Q(title__icontains=self.query) | Q(content__icontains=self.query))

                results = self.model.objects.select_related('category').filter(Q(title__icontains=self.query) | Q(content__icontains=self.query))
                page = self.request.GET.get('page', 1)
                paginator = Paginator(results, 6)
                try:
                    context['results'] = paginator.page(page)
                except PageNotAnInteger:
                    context['results'] = paginator.page(1)
                except EmptyPage:
                    context['results'] = paginator.page(paginator.num_pages)
                context['query'] = self.query

        return context



class UserReactionView(View):
    template_name = 'blog/single-blog.html'
    
    def get(self, request, *args, **kwargs):
        article_id = self.request.GET.get('article_id')
        article = Article.objects.get(id=article_id)
        like = self.request.GET.get('like')
        current_user, _ = IpUser.objects.get_or_create(ip=self.request.META['REMOTE_ADDR'])
        
        if like and (current_user not in article.ip_like.all()):
            article.likes += 1
            article.ip_like.add(current_user)
            article.save()
        else:
            article.likes -= 1
            article.ip_like.remove(current_user)
            delete_ip_user = IpUser.objects.get(ip=current_user)
            delete_ip_user.delete()
            article.save()
            
        data = {
            'likes': article.likes,
        }
        return JsonResponse(data)


class CreateCommentView(View):
    template_name = 'blog/single-blog.html'

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get('article_id')
        name = self.request.POST.get('name')
        comment = self.request.POST.get('comment')
        honeypot = self.request.POST.get('honeypot')
        article = Article.objects.get(id=article_id)

        if honeypot == '':
            new_comment = article.comments.create(name=name, comment=comment)

        total_comments = article.comments.count()

        comment = [{
            'name': new_comment.name, 
            'comment': new_comment.comment, 
            'honeypot': honeypot, 
            'total_comments': total_comments
            }]
        return JsonResponse(comment, safe=False)


class SubscribeView(View):

    def post(self, request, *args, **kwargs):
        form_subscr = SubscriberForm(request.POST or None)
        article = Article.objects.first()

        if form_subscr.is_valid():
            new = form_subscr.cleaned_data['email']
            new_user = Subscriber()

            if Subscriber.objects.filter(email=new).exists():
                is_exists = False
                
                json_data = {
                    'not_added': is_exists
                }

                return JsonResponse(json_data)

            else:
                new_user.email = new
                new_user.save()
                is_exists = True

                json_data = {
                    'added': is_exists
                }

                return JsonResponse(json_data)


        else:
            messages.add_message(request, messages.INFO, 'Чтото не то')
            form_subscr = SubscriberForm()



class ContactView(CategoryMixin, View):

    template_name = 'blog/contact.html'

    def get(self, request, **kwargs):
        form = ContactForm()
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(subject, message, 'arvillist@gmail.com', email)
            return redirect(reverse('home'))
        else:
            form = ContactForm()

        context = {
            'form': form
            }
        return render(request, self.template_name, context)


def contact_view(request):
     form = ContactForm(request.POST or None)
     context = {}
     context['form'] = ContactForm(request.POST or None)
     context['category_from_mixin'] = Category.objects.all()[:2]
     context['search_form'] = SearchForm()

     if request.method == "POST":
         if form.is_valid():
              name = form.cleaned_data['name']
              email = form.cleaned_data['email']
              subject = form.cleaned_data['subject']
              message = form.cleaned_data['message']
              
              send_mail(subject, message, 'arvillist@gmail.com', [email])
              return redirect(reverse('thanks'))
         else:
            form = ContactForm()
     else:
        form = ContactForm()

     return render(request, 'blog/contact.html', context)


def thanks(request):
    context = {}
    context['form'] = ContactForm(request.POST or None)
    context['category_from_mixin'] = Category.objects.all()[:2]
    context['search_form'] = SearchForm()
    return render(request, '_parts/thanks.html', context)



def import_csv(request):
    """  тестовые данные """
    list_news = ['hi-tech', 'Politic']
    list_tags = ['tech', 'politic']
    with open('D:/projects/BLOG_WITH_TUTORIALS/myproject/blog/data_articles_two.csv', encoding='utf-8', newline='') as f_obj:
        spamreader = csv.reader(f_obj)
        for row in spamreader:
            # print('category', row[0])
            # print('tag', row[1])
            # print('Заголовок статьи', row[2])
            # print('Фото статьи', row[3])
            link = 'http:' + row[3]
            # print('Фото статьи', link)
            convert = row[4].replace("'", '')
            # print(convert)

            temp = Article()
            temp_category, _ = Category.objects.get_or_create(name=row[0])
            temp.category = temp_category
            temp.save()
            temp.title = row[2]
            temp.tags = temp.tags.add(row[1])
            r = link
            path_to_media = 'D:/projects/LAST_BLOG/django/media/articles/'
            temp.image = wget.download(r, path_to_media)
            temp.content = convert.strip('[]')
            temp.save()

    return HttpResponse('Ok')
