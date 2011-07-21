from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from gallery.models import Album, Photo

def index(request):
    album_list = Album.objects.all()
    return render_to_response('gallery/index.html', {'album_list': album_list})

def album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    photo_list = Photo.objects.filter(album=album_id)
    return render_to_response('gallery/album.html', {'album': album, 'photo_list': photo_list})
