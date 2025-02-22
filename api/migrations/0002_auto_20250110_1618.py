# Generated by Django 3.2 on 2025-01-10 08:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='create_time',
            field=models.TimeField(auto_now=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='news',
            name='news_info',
            field=models.CharField(default=django.utils.timezone.now, max_length=277, verbose_name='新闻信息'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='title',
            field=models.CharField(default=1, max_length=50, verbose_name='标题'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='url',
            field=models.CharField(default=23, max_length=100, verbose_name='路由'),
            preserve_default=False,
        ),
    ]
