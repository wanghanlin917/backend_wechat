from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(verbose_name="标题", max_length=50)
    news_info = models.CharField(verbose_name="新闻信息", max_length=277)
    url = models.CharField(verbose_name="路由", max_length=100)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class User(models.Model):
    avatar = models.CharField(verbose_name="头像", max_length=256, default="")
    mobile = models.CharField(verbose_name="电话号码", max_length=11)
    nickName = models.CharField(verbose_name="用户名", max_length=128, default="")


class HouseInformation(models.Model):
    name = models.CharField(verbose_name="户主姓名", max_length=50)
    point = models.CharField(verbose_name="小区信息", max_length=32)
    building = models.CharField(verbose_name="小区楼栋信息",max_length=32)
    room = models.CharField(verbose_name="小区房间信息",max_length=32)
    mobile = models.CharField(verbose_name="电话号码", max_length=11)
    gender = models.IntegerField(verbose_name="性别", choices=((0, '女'), (1, '男')))
    idcardFront = models.CharField(verbose_name="身份证正面", max_length=64)
    idcardBack = models.CharField(verbose_name="身份证反面", max_length=64)
    user = models.ForeignKey(verbose_name='用户', to=User, on_delete=models.CASCADE)
