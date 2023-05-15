import uuid
from datetime import timedelta
from typing import Any

from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenViewBase
from django.db.models import Avg, Count
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from Songs.rest_API.models import Song, Album, Singer, AlbumSong, UserProfile
from Songs.rest_API.serializers import SongSerializer, AlbumSerializer, SingerSerializer, AlbumSongSerializer, \
    StatisticsSerializer, BulkAddSingerWithAlbums, UserProfileSerializer, \
    MyTokenObtainPairSerializer, UserSerializer
from rest_framework.decorators import api_view
from django.db.models import Count
from rest_framework import generics



@api_view(['GET', 'POST'])
def SongView(request):
    # get all songs
    # serialize them
    # return json
    if request.method == 'GET':
        playlist = Song.objects.all()
        serializer = SongSerializer(playlist, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def song_detail(request, id):
    try:
        song = Song.objects.get(pk=id)
    except Song.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SongSerializer(song)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def AlbumView(request):
    # get all albums
    # serialize them
    # return json
    if request.method == 'GET':
        album = Album.objects.all()
        serializer = AlbumSerializer(album, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def album_detail(request, id):
    try:
        album = Album.objects.get(pk=id)
    except Album.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def SingerView(request):
    # get all singers
    # serialize them
    # return json
    if request.method == 'GET':
        singer = Singer.objects.all()
        serializer = SingerSerializer(singer, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SingerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def singer_detail(request, id):
    try:
        singer = Singer.objects.get(pk=id)
    except Singer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SingerSerializer(singer)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SingerSerializer(singer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        albums = singer.albums.all()
        albums.delete()
        singer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def AlbumSongView(request, format=None):
    if request.method == 'GET':
        albumsong = AlbumSong.objects.all()
        serializer = AlbumSongSerializer(albumsong, many=True)

        return Response(serializer.data)

    if request.method == 'POST':
        serializer = AlbumSongSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'PUT', 'DELETE'])
def AlbumSongDetail(request, id):

    try:
        albumsong = AlbumSong.objects.get(pk=id)
    except albumsong.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlbumSongSerializer(albumsong)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AlbumSongSerializer(albumsong, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        albumsong.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Statistics(APIView):
    @api_view(['GET'])
    def statistics_albums(request):
        # songs ordered by the average of their albums no_of_songs
        statistics = Album.objects.annotate(
            avg=Avg('no_of_songs'),
            song_count=Count('albumsong')
        ).order_by('-avg')

        serializer = StatisticsSerializer(statistics, many=True)
        return Response(serializer.data)


class BulkAddView(APIView):
    @csrf_exempt
    @api_view(['POST'])
    def bulkAddSingertoAlbum(request):
        serializer = BulkAddSingerWithAlbums(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Singer and albums added successfully.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = "id"
    queryset = UserProfile.objects.all()


@api_view(['GET'])
def UserView(request, format=None):
    if request.method == 'GET':
        u = UserProfile.objects.all()
        serializer = UserProfileSerializer(u, many=True)
        return Response(serializer.data)


class LoginView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    View to register a new user.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        activation_expiry_date = str(timezone.now() + timedelta(minutes=10))
        activation_code = str(uuid.uuid4())
        data = request.data.copy()
        data["activation_code"] = activation_code
        data["activation_expiry_date"] = activation_expiry_date
        data["active"] = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"activation_code": activation_code},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserActivationView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        activation_code = request.data.get("activation_code")
        try:
            user_profile: UserProfile = UserProfile.objects.get(
                activation_code=activation_code
            )
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "Activation code not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_profile.activation_expiry_date < timezone.now():
            return Response(
                {"error": "Activation code expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        if user_profile.active:
            return Response(
                {"success": "Account already active"}, status=status.HTTP_200_OK
            )

        user_profile.active = True
        user_profile.save()
        return Response(
            {"success": "User profile activated"}, status=status.HTTP_200_OK
        )
