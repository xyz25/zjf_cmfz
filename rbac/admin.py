from django.contrib import admin

# Register your models here.
from rbac.models import Permission, Role
from index.models import Admin

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Admin)
