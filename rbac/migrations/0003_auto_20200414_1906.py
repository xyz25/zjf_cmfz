# Generated by Django 2.0.6 on 2020-04-14 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_auto_20200414_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='title',
            field=models.CharField(max_length=32, verbose_name='标题'),
        ),
    ]
