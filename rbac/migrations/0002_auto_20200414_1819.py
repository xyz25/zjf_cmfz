# Generated by Django 2.0.6 on 2020-04-14 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='title',
            field=models.CharField(db_column='url标题', max_length=32, verbose_name='标题'),
        ),
    ]
