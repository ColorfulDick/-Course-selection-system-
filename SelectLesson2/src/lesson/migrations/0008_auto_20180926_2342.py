# Generated by Django 2.0.7 on 2018-09-26 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0007_auto_20180926_1937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='rteahcer',
            new_name='rteacher',
        ),
        migrations.AddField(
            model_name='result',
            name='rlessontype',
            field=models.CharField(default='', max_length=30, verbose_name='课程类型'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='time',
            field=models.CharField(choices=[('上午1-2节', '上午1-2节'), ('上午3-4节', '上午3-4节'), ('下午5-6节', '下午5-6节'), ('下午7-8节', '下午7-8节'), ('晚上9-10节', '晚上9-10节'), ('晚上11-12节', '晚上11-12节')], max_length=30, verbose_name='上课时间'),
        ),
    ]
