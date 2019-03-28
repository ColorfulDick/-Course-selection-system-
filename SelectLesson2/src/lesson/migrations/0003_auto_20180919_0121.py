# Generated by Django 2.0.7 on 2018-09-18 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0002_auto_20180918_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='学生姓名')),
                ('class_name', models.CharField(max_length=30, verbose_name='班级')),
                ('username', models.CharField(max_length=30, verbose_name='学号')),
                ('password', models.CharField(max_length=30, verbose_name='密码')),
            ],
            options={
                'verbose_name_plural': '学生信息',
                'verbose_name': '学生信息',
            },
        ),
        migrations.AlterField(
            model_name='result',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='class_name2', to='lesson.Students', verbose_name='所在班级'),
        ),
        migrations.AlterField(
            model_name='result',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='name2', to='lesson.Students', verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='result',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='username2', to='lesson.Students', verbose_name='学号'),
        ),
        migrations.DeleteModel(
            name='UserForm',
        ),
    ]