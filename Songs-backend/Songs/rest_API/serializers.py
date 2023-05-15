from collections import OrderedDict
from typing import Any, Type

from rest_framework import serializers
from Songs.rest_API.models import Song, Album, Singer, AlbumSong, UserProfile
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import RefreshToken, TokenObtainPairSerializer


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id',
                  'name',
                  'singer',
                  'duration',
                  'likes',
                  'dislikes']

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value

    def validate_singer(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Singer name must be at least 2 characters long.")
        return value

    def validate_duration(self, value):
        if value.total_seconds() < 30:
            raise serializers.ValidationError("Duration must be at least 30 seconds.")
        return value

    def validate_likes(self, value):
        if value < 0:
            raise serializers.ValidationError("Likes must be a non-negative integer.")
        return value

    def validate_dislikes(self, value):
        if value < 0:
            raise serializers.ValidationError("Dislikes must be a non-negative integer.")
        return value


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id',
                  'name',
                  'singer',
                  'duration',
                  'year_of_release',
                  'no_of_songs']

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value


    def validate_duration(self, value):
        if value.total_seconds() / 60 < 0:
            raise serializers.ValidationError("Duration can not be a negative number.")
        return value

    def validate_year_of_release(self, value):
        if value < 1900:
            raise serializers.ValidationError("Year of release must be after 1900.")
        return value

    def validate_no_of_songs(self, value):
        if value < 0:
            raise serializers.ValidationError("Number of songs must be a positive number.")
        return value


class SingerSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Singer
        fields = ['id',
                  'stage_name',
                  'name',
                  'age',
                  'dob',
                  'star_sign',
                  'albums']

    def validate_stage_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Stage name must be at least 2 characters long.")
        return value

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value

    def validate_age(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError("Age must be between 0 and 100")
        return value

    def validate_dob(self, value):
        if value.year < 1900:
            raise serializers.ValidationError("DOB must be after 1900")
        return value

    def validate_star_sign(self, value):
        star_signs = ["Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer",
                      "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn"]
        if value not in star_signs:
            raise serializers.ValidationError("Star sign must be one of the following:"
                                              " {}".format(", ".join(star_signs)))
        return value


class BulkAddSingerWithAlbums(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    stage_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    dob = serializers.DateField()
    star_sign = serializers.CharField(max_length=100)
    albums = AlbumSerializer(many=True)

    def create(self, validated_data):
        albums_data = validated_data.pop('albums')
        singer = Singer.objects.create(**validated_data)
        for album_data in albums_data:
            album_data.pop('singer', None)
            Album.objects.create(singer=singer, **album_data)
        return singer


class AlbumSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumSong
        fields = ['album_id',
                  'song_id']


class StatisticsSerializer(serializers.ModelSerializer):
    avg = serializers.IntegerField(read_only=True)
    song_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'avg', 'song_count']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError('Password must contain at least one digit.')

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')

        return value


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            "user",
            "u_first_name",
            "u_last_name",
            "u_date_of_birth",
            "u_bio",
            "u_location",
            "activation_code",
            "activation_expiry_date",
            "active",
        )

    def create(self, validated_data: OrderedDict[str, Any]) -> UserProfile:
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        user = UserProfile.objects.get(user_id = self.user.username)

        refresh["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "u_first_name": user.u_first_name,
            "u_last_name": user.u_last_name,
            "u_bio": user.u_bio,
            "u_date_of_birth": f'{user.u_date_of_birth}',
            "u_location": user.u_location,
        }

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
