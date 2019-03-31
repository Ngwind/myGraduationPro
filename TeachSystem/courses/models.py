from datetime import datetime

from django.db import models
from django.conf import settings


# 课程表
class Course(models.Model):
    courseName = models.CharField(verbose_name="课程名称", max_length=100, null=False)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="添加人")
    createdate = models.DateTimeField("添加时间", default=datetime.now)
    editdate = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.courseName


# 视频资源表
class Video(models.Model):
    chapterId = models.CharField(verbose_name="章节号", max_length=100)
    videoName = models.CharField(verbose_name="视频名称", max_length=100, null=False)
    videoUrl = models.CharField(verbose_name="视频链接地址", max_length=500, null=False)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="添加人")
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, verbose_name="所属课程id")
    createdate = models.DateTimeField("添加时间", default=datetime.now)
    editdate = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        verbose_name = "视频资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.videoName


# 视频学习进度表
class CourseProgress(models.Model):
    video = models.ForeignKey(to="Video", on_delete=models.CASCADE, verbose_name="视频id")
    student = models.ForeignKey(to="users.Student", on_delete=models.CASCADE, verbose_name="学生id")
    progress = models.CharField(verbose_name="观看进度", max_length=100, default="0")
    editdate = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        verbose_name = "学习进度"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.video.videoName+"-"+self.student.username


# 课程成绩表
class Scores(models.Model):
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, verbose_name='课程id')
    student = models.ForeignKey(to='users.Student', on_delete=models.CASCADE, verbose_name='学生id')
    score = models.IntegerField(verbose_name="分数", null=True)

    class Meta:
        verbose_name = "学生成绩"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.courseName+"-"+self.student.username
