from django.contrib import admin

# Register your models here.
from album.models import Album, Chapter

admin.site.register(Album)
admin.site.register(Chapter)

