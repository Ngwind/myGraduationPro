# Generated by Django 2.0 on 2019-04-19 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190413_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(default='', max_length=400, verbose_name='反馈内容')),
                ('createdate', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('openid', models.CharField(default='', max_length=200, verbose_name='openid')),
            ],
            options={
                'verbose_name': '用户反馈',
                'verbose_name_plural': '用户反馈',
            },
        ),
    ]