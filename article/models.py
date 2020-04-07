from django.db import models


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=20)
    cate = models.BooleanField()
    user_id = models.IntegerField()

    class Meta:
        db_table = 'course'


class Count(models.Model):
    title = models.CharField(max_length=20)
    counts = models.IntegerField()
    last_time = models.DateTimeField(auto_now_add=True)
    course_id = models.IntegerField()

    class Meta:
        db_table = 'count'
    