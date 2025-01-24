# Generated by Django 3.2 on 2025-01-24 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_houseinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='houseinformation',
            name='status',
            field=models.IntegerField(choices=[(0, '未验证'), (1, '验证中'), (2, '验证成功')], default=0, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='houseinformation',
            name='gender',
            field=models.IntegerField(choices=[(0, '女'), (1, '男')], default=0, verbose_name='性别'),
        ),
    ]