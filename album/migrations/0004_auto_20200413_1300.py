# Generated by Django 2.0.6 on 2020-04-13 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0003_auto_20200413_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='chapter_count',
            field=models.IntegerField(null=True),
        ),
    ]
