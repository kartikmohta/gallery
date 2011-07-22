import os
import Image
from django.template import Library

register = Library()

def thumbnail(file, size='128x128'):
    """
    Example:
    <img src="object.get_image_url" alt="original image" />
    <img src="object.image|thumbnail" alt="image resized to default 200x200 format" />
    <img src="object.image|thumbnail:"200x300" alt="image resized to 200x300" />

    The filter is applied to a image field (not the image url get from
    get_image_url method of the model), supposing the image filename is
    "image.jpg", it checks if there is a file called "image_200x200.jpg" or
    "image_200x300.jpg" on the second case, if the file isn't there, it resizes
    the original image, finally it returns the proper url to the resized image.
    """

    if file:
        # defining the size
        x, y = [int(x) for x in size.split('x')]
        # defining the filename and the miniature filename
        basename, format = file.path.rsplit('.', 1)
        baseurl, _format = file.url.rsplit('.', 1)

        miniature_filename = basename + '_' + size + '.' +  format
        miniature_url = baseurl + '_' + size + '.' +  format

        if os.path.exists(miniature_filename) and os.path.getmtime(file.path) > os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
        # if the image wasn't already resized, resize it
        if not os.path.exists(miniature_filename):
            image = Image.open(file.path)
            image.thumbnail([x, y], Image.ANTIALIAS)
            try:
                image.save(miniature_filename, image.format, quality=90, optimize=1)
            except:
                image.save(miniature_filename, image.format, quality=90)
        return miniature_url



    return ''

register.filter(thumbnail)
