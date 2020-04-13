# Generated by Django 2.0.6 on 2020-04-13 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='broadcast',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='score',
            field=models.SmallIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='time_long',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='url',
            field=models.FileField(upload_to='video'),
        ),
    ]