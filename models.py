from django.db import models
from os import unlink
from os.path import splitext
from uuid import uuid4
from pyexiv2 import ImageMetadata
from glob import glob

PHOTO_FILENAME_MAX_LENGTH = 255

def getPhotoUploadToFilename(instance, filename):
    instance.user_filename = filename[:PHOTO_FILENAME_MAX_LENGTH]
    basename, ext = splitext(filename)
    new_filename = uuid4().hex + ext
    return new_filename

class Photo(models.Model):
    image = models.ImageField(upload_to=getPhotoUploadToFilename, height_field='height', width_field='width',
            max_length=PHOTO_FILENAME_MAX_LENGTH)
    user_filename = models.CharField(max_length=PHOTO_FILENAME_MAX_LENGTH, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    date_taken = models.DateTimeField(null=True)
    votes = models.IntegerField(default=0)
    album = models.ForeignKey('Album', null=True, blank=True, on_delete=models.SET_NULL)
    private = models.BooleanField(default=False)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __unicode__(self):
        return self.caption

    def clean(self):
        #TODO: Check filesize and reject very large files
        print self.image.size
        print self.image.height
        print self.image.width

    def save(self, *args, **kwargs):
        if self.pk == None: # Only do this when adding a new item
            metadata = ImageMetadata.from_buffer(self.image.read(1024*1024)) # 1MB should be enough to get Exif tags
            metadata.read()
            self.date_taken = metadata['Exif.Photo.DateTimeOriginal'].value
        super(Photo, self).save(*args, **kwargs) # Call the "real" save() method.

    def delete(self):
        basename, ext = splitext(self.image.path)
        for file in glob(basename+'*'+ext):
            unlink(file)
        super(Photo, self).delete()

class Album(models.Model):
    PRIVACY_CHOICES =(
            ('public', 'Public'),
            ('link', 'Only with link'),
            ('private', 'Private'),
            )
    name = models.CharField(max_length=100)
    privacy = models.CharField(max_length=7, default='public', choices=PRIVACY_CHOICES)
    parent_album = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    cover_photo = models.OneToOneField('Photo', related_name='+', blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name
