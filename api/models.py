from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(verbose_name="标题",max_length=50)
    news_info = models.CharField(verbose_name="新闻信息", max_length=277)
    url = models.CharField(verbose_name="路由", max_length=100)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

class User(models.Model):
    mobile = models.CharField(verbose_name="电话号码",max_length=11)

