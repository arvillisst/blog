# Generated by Django 2.2.1 on 2019-06-01 12:37

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_subscriber_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
