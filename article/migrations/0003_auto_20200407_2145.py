# Generated by Django 2.0.6 on 2020-04-07 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20200407_2143'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Count',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
