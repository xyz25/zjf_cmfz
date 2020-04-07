from django.db import models


# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    broadcast = models.CharField(max_length=20)
    chapter_count = models.IntegerField()
    content = models.TextField()
    score = models.SmallIntegerField()
    publish_time = models.DateTimeField(auto_now_add=True)
    img_src = models.CharField(max_length=40)

    class Meta:
        db_table = 'album'


class Chapter(models.Model):
    title = models.CharField(max_length=20)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    url = models.CharField(max_length=20)
    time_long = models.SmallIntegerField()
    album_id = models.IntegerField()

    class Meta:
        db_table = 'chapter'
