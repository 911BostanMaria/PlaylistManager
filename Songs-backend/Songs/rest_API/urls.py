"""Songs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView

from Songs.rest_API import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from Songs.rest_API.views import LoginView, UserRegistrationView, UserActivationView, UserDetail

urlpatterns = [
    path('admin/', admin.site.urls),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    path('songs/', views.SongView),
    path('songs/<int:id>/', views.song_detail),

    path('albums/', views.AlbumView),
    path('albums/<int:id>/', views.album_detail),

    path('singers/<int:id>/', views.singer_detail),
    path('singers/', views.SingerView),
    path('many/', views.AlbumSongView),
    path('stats/', views.Statistics.statistics_albums),
    path('bulkadd/', views.BulkAddView.bulkAddSingertoAlbum),
    path('login/', LoginView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', UserRegistrationView.as_view(), name="register"),
    path("activate/", UserActivationView.as_view(), name="activate-user"),
    path('users/<int:id>/', UserDetail.as_view(), name='user-detail'),
    path('users/', views.UserView),
]


urlpatterns = format_suffix_patterns(urlpatterns)
