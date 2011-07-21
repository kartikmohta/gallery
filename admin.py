from gallery.models import Photo, Album
from django.contrib import admin

class PhotoAdmin(admin.ModelAdmin):
    fields = ['image', 'caption', 'album', 'private']

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album)
