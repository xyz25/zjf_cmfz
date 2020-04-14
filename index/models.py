from django.db import models
from rbac.models import Role


# Create your models here.

class Admin(models.Model):
    name = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=20)
    # to='app_name.model_name'
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='rbac.Role', blank=True)

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return self.name
