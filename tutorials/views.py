from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from .models import Category, Tutorial, IpUser
from django.views.generic import ListView, View
from hitcount.views import HitCountDetailView
from blog.mixins import CategoryMixin
from .forms import CommentForm
import csv
import wget

class CategoryView(ListView, CategoryMixin):
    """ Страница со списком туториалов """
    model = Category
    template_name = 'tutorials/tutorials_index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data(*args, **kwargs)
        context['categories'] = self.model.objects.all()
        article_list = self.model.objects.order_by('created')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(article_list, 6)
        try:
            context['cats'] = paginator.page(page)
        except PageNotAnInteger:
            context['cats'] = paginator.page(1)
        except EmptyPage:
            context['cats'] = paginator.page(paginator.num_pages)
        return context


class TutorialDetailView(HitCountDetailView, CategoryMixin):
    """ Страница с детальной информацией """
    template_name = 'tutorials/single-tutorial.html'
    model = Tutorial
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(TutorialDetailView, self).get_context_data(*args, **kwargs)
        context['art'] = self.get_object().category.tutorial_set.all()
        context['article'] = self.get_object()

        context['form'] = CommentForm()
        context['article_comments'] = self.get_object().comments.all().order_by('-created')
        print(self.get_object().comments.all())
        
        # похожие статьи
        # article_tags_ids = self.get_object().tags.values_list('id', flat=True)
        # similar_articles = self.model.objects.filter(tags__in=article_tags_ids).exclude(id=self.get_object().id)
        # similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
        # context['similar_articles'] = similar_articles

        # следующая и предыдущая статьи
        context['prev_post'] = self.get_object().category.tutorial_set.filter(id__lt=self.object.id).order_by('id').reverse().first()
        context['next_post'] = self.get_object().category.tutorial_set.filter(id__gt=self.object.id).order_by('id').first()
        return context


class UserReactionView(View):
    template_name = 'tutorials/single-tutorial.html'
    
    def get(self, request, *args, **kwargs):
        article_id = self.request.GET.get('article_id')
        article = Tutorial.objects.get(id=article_id)
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
    template_name = 'tutorials/single-tutorial.html'

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get('article_id')
        name = self.request.POST.get('name')
        comment = self.request.POST.get('comment')
        honeypot = self.request.POST.get('honeypot')
        
        article = Tutorial.objects.get(id=article_id)

        if honeypot == '':
            new_comment = article.comments.create(name=name, comment=comment)
            
        comment = [{'name': new_comment.name, 'comment': new_comment.comment, 'honeypot': honeypot}]
        return JsonResponse(comment, safe=False)




def import_csv_tutorials(request):
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

            temp = Tutorial()
            temp_category, _ = Category.objects.get_or_create(name=row[0])
            temp.category = temp_category
            temp.save()
            temp.title = row[2]
            temp.tags = temp.tags.add(row[1])
            r = link
            path_to_media = 'D:/projects/LAST_BLOG/django/media/tutorials/'
            temp.image = wget.download(r, path_to_media)
            temp.content = convert.strip('[]')
            temp.save()

    return HttpResponse('Ok')