from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(verbose_name="标题",max_length=50)
    news_info = models.CharField(verbose_name="新闻信息", max_length=277)
    url = models.CharField(verbose_name="路由", max_length=100)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

class User(models.Model):
    avatar = models.CharField(verbose_name="头像", max_length=256,default="")
    mobile = models.CharField(verbose_name="电话号码",max_length=11)
    nickName = models.CharField(verbose_name="用户名", max_length=128,default="")

