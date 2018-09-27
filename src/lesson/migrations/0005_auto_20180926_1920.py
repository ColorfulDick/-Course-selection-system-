# Generated by Django 2.0.7 on 2018-09-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0004_students_u_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='result',
            name='classroom',
        ),
        migrations.RemoveField(
            model_name='result',
            name='lessonname',
        ),
        migrations.RemoveField(
            model_name='result',
            name='name',
        ),
        migrations.RemoveField(
            model_name='result',
            name='teahcer',
        ),
        migrations.RemoveField(
            model_name='result',
            name='time',
        ),
        migrations.RemoveField(
            model_name='result',
            name='username',
        ),
        migrations.RemoveField(
            model_name='result',
            name='week',
        ),
        migrations.AddField(
            model_name='result',
            name='class_name2',
            field=models.CharField(default='', max_length=30, verbose_name='班级'),
        ),
        migrations.AddField(
            model_name='result',
            name='classroom2',
            field=models.CharField(default='', max_length=30, verbose_name='上课教室'),
        ),
        migrations.AddField(
            model_name='result',
            name='lessonname2',
            field=models.CharField(default='', max_length=30, verbose_name='课程名称'),
        ),
        migrations.AddField(
            model_name='result',
            name='name2',
            field=models.CharField(default='', max_length=30, verbose_name='学生姓名'),
        ),
        migrations.AddField(
            model_name='result',
            name='teahcer2',
            field=models.CharField(default='', max_length=30, verbose_name='任课老师'),
        ),
        migrations.AddField(
            model_name='result',
            name='time2',
            field=models.CharField(default='', max_length=30, verbose_name='上课时间'),
        ),
        migrations.AddField(
            model_name='result',
            name='username2',
            field=models.CharField(default='', max_length=30, verbose_name='学号'),
        ),
        migrations.AddField(
            model_name='result',
            name='week2',
            field=models.CharField(default='', max_length=30, verbose_name='起始-结束周'),
        ),
    ]
