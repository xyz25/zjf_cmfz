# Generated by Django 2.0.6 on 2020-04-14 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20200414_1906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='roles',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
