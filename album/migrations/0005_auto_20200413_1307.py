# Generated by Django 2.0.6 on 2020-04-13 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0004_auto_20200413_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='chapter_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
