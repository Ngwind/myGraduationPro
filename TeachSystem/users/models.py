from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# 学生表
class Student(models.Model):

    gender_choices = (
        ('male', '男'),
        ('female', '女')
    )

    gender = models.CharField('性别', max_length=10, choices=gender_choices, default='female')
    studentId = models.CharField('学号', max_length=10, primary_key=True)
    username = models.CharField('姓名', max_length=20, null=False)
    college = models.CharField('学院', max_length=50, null=False)
    userclass = models.CharField('班级', max_length=50, null=False)
    password = models.CharField('密码', max_length=20, null=False, default='123456')
    createdate = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "学生管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}{1}".format(self.studentId, self.username)


# 教师表
class Teacher(AbstractUser):
    college = models.CharField('学院', max_length=50, null=False)

    class Meta:
        verbose_name = "教师管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.first_name+self.last_name


# 微信openid记录表
class Openid(models.Model):
    openid = models.CharField('openid', max_length=200, default=None)
    studentid = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="学号")
    createdate = models.DateTimeField("添加时间", default=datetime.now)
    editdate = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        verbose_name = "openid记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.studentid
