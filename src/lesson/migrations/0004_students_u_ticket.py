# Generated by Django 2.0.7 on 2018-09-19 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0003_auto_20180919_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='u_ticket',
            field=models.CharField(max_length=30, null=True),
        ),
    ]