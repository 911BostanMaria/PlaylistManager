from django.contrib.auth.models import User
from django.db import models


class Song(models.Model):
    name = models.CharField(max_length=100)
    singer = models.CharField(max_length=100)
    duration = models.DurationField()
    likes = models.BigIntegerField()
    dislikes = models.BigIntegerField()

    def __str__(self):
        return str(self.id) + '. ' + self.name + ' by ' + self.singer + ', ' + str(self.duration) + ' min, ' \
               + ' Likes: ' + str(self.likes) + ', Dislikes: ' + str(self.dislikes)


class Singer(models.Model):
    stage_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    age = models.BigIntegerField()
    dob = models.DateField()
    star_sign = models.CharField(max_length=100)

    def __str__(self):
        return self.stage_name + ' (' + self.name + '),' + str(self.age) + ', ' + str(self.dob) + ', ' + self.star_sign


class Album(models.Model):
    name = models.CharField(max_length=100)
    singer = models.ForeignKey(Singer, related_name='albums', on_delete=models.CASCADE)
    duration = models.DurationField()
    year_of_release = models.BigIntegerField()
    no_of_songs = models.BigIntegerField()



    def __str__(self):
        return self.name + ', ' + self.singer.stage_name + ', ' + str(self.duration) + ' min ' + str(
            self.year_of_release) \
               + ' ' + str(self.no_of_songs)


class AlbumSong(models.Model):
    # many-to-many relationship
    # a single album can contain multiple songs
    # and a single song can be included in multiple albums.
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    copies_sold = models.BigIntegerField()
    grammys = models.BigIntegerField()

    def __str__(self):
        return str(self.song_id) + ' ' + str(self.album_id)


class UserProfile(models.Model):
    u_first_name = models.CharField(max_length=100)
    u_last_name = models.CharField(max_length=100)
    u_date_of_birth = models.DateField()
    u_bio = models.CharField(max_length=500)
    u_location = models.CharField(max_length=100)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", to_field="username"
    )
    activation_code = models.CharField(max_length=36)
    activation_expiry_date = models.DateTimeField()
    active = models.BooleanField()