# Generated by Django 2.2.1 on 2019-05-25 10:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
