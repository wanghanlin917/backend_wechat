from django.db import models

# Create your models here.
class News(models.Model):
    news_info = models.CharField(verbose_name="新闻信息", max_length=277)