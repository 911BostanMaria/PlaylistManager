from django.contrib import admin
from Songs.rest_API.models import Singer, Song, Album, AlbumSong

admin.site.register(Song)
admin.site.register(Singer)
admin.site.register(Album)
admin.site.register(AlbumSong)
