# Generated by Django 2.0.6 on 2020-04-09 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200409_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='details',
            field=models.TextField(null=True),
        ),
    ]