# Generated by Django 2.0.6 on 2020-04-13 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0006_auto_20200413_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='size',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
