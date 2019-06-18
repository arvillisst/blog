from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from hitcount.models import HitCountMixin, HitCount
from taggit.managers import TaggableManager
import unidecode  # pip install unidecode
from django.utils.text import slugify as _slugify, Truncator


def slugify(value, truncate_chars):
    '''Truncator и slugify - стандартные утилиты Django. Функция ограничивает текст до заданного количества символов.'''
    return Truncator(_slugify(unidecode.unidecode(value))).chars(truncate_chars, truncate='')


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, 120)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


def generate_filename(instance, filename):
    filename = instance.slug + '.jpg'
    return '{0}/{1}'.format(instance, filename)


class Article(models.Model, HitCountMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=225, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    image = models.ImageField(upload_to=generate_filename, blank=True, verbose_name='Фото')
    content = RichTextUploadingField(blank=True, default='')
    comments = GenericRelation('comment')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    ip_like = models.ManyToManyField('IpUser', verbose_name='Кто лайкнул (IP)', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    tags = TaggableManager(blank=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, 225)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return 'Статья {0} из категории {1}'.format(self.title, self.category.name)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'category': self.category.slug, 'slug': self.slug})


class IpUser(models.Model):
    ip = models.CharField(max_length=50, verbose_name='IP строка')

    def __str__(self):
        return f'{self.ip}'


class Comment(models.Model):
    name = models.CharField(max_length=64, verbose_name='Имя пользователя')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.name}'



class Subscriber(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'


