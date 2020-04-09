from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    religions_name = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    salt = models.CharField(max_length=40)
    status = models.BooleanField()
    img_src = models.ImageField(upload_to='user',null=True)
    last_login_time = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True)
    address = models.CharField(max_length=40)
    email = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'
