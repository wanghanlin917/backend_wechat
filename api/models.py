from django.db import models
import django.utils.timezone as timezone


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
    building = models.CharField(verbose_name="小区楼栋信息", max_length=32)
    room = models.CharField(verbose_name="小区房间信息", max_length=32)
    mobile = models.CharField(verbose_name="电话号码", max_length=11)
    gender = models.IntegerField(verbose_name="性别", choices=((0, '女'), (1, '男')), default=0)
    idcardFront = models.CharField(verbose_name="身份证正面", max_length=128)
    idcardBack = models.CharField(verbose_name="身份证反面", max_length=128)
    user = models.ForeignKey(verbose_name='用户', to=User, on_delete=models.CASCADE)
    status_choices = ((0, '未验证'), (1, '验证中'), (2, '验证成功'))
    status = models.IntegerField(verbose_name="状态", choices=status_choices, default=0)


class RepairProject(models.Model):
    name = models.CharField(verbose_name="报修项目", max_length=32)

class Repair(models.Model):
    houseId = models.OneToOneField(verbose_name="房屋信息", to=HouseInformation, on_delete=models.CASCADE)
    repairItemId = models.OneToOneField(verbose_name="维修项目", to=RepairProject, on_delete=models.CASCADE)
    description = models.CharField(verbose_name="问题描述", max_length=200)
    mobile = models.CharField(verbose_name="电话", max_length=11)
    user = models.ForeignKey(verbose_name='用户', to=User, on_delete=models.CASCADE)
    appointment = models.DateTimeField(verbose_name="预约时间", default=timezone.now)
class RepairImg(models.Model):
    url = models.CharField(verbose_name="上传报修图片",max_length=128)
    repairId = models.ForeignKey(verbose_name='报修单',to=Repair, on_delete=models.CASCADE)