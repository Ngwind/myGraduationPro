# Generated by Django 2.0 on 2019-03-30 21:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(max_length=100, verbose_name='课程名称')),
                ('createdate', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('editdate', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
            },
        ),
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.CharField(default='0', max_length=100, verbose_name='观看进度')),
                ('editdate', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '学习进度',
                'verbose_name_plural': '学习进度',
            },
        ),
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(null=True, verbose_name='分数')),
            ],
            options={
                'verbose_name': '课程成绩',
                'verbose_name_plural': '课程成绩',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapterId', models.CharField(max_length=100, verbose_name='章节号')),
                ('videoName', models.CharField(max_length=100, verbose_name='视频名称')),
                ('videoUrl', models.CharField(max_length=500, verbose_name='视频链接地址')),
                ('createdate', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('editdate', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='所属课程id')),
            ],
            options={
                'verbose_name': '视频资源',
                'verbose_name_plural': '视频资源',
            },
        ),
    ]