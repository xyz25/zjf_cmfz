# Generated by Django 2.0.6 on 2020-04-09 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200409_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img_src',
            field=models.ImageField(null=True, upload_to='user'),
        ),
    ]