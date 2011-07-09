from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    caption = models.CharField(max_length=200, blank=True)
    date_taken = models.DateTimeField()
    votes = models.IntegerField(default=0)
    album = models.ForeignKey('Album', null=True, on_delete=models.SET_NULL)
    private = models.BooleanField(default=False)

class Album(models.Model):
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('link', 'Only with link'),
        ('private', 'Private'),
    )
    name = models.CharField(max_length=100)
    privacy = models.CharField(max_length=7, default='public', choices=PRIVACY_CHOICES)
    parent_album = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    cover_photo = models.OneToOneField('Photo', related_name='+')
