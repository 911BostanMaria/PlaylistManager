from datetime import timedelta
from Songs.rest_API.models import *
from django.test import TestCase


class SongModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="melodie", singer="eu", duration=timedelta(minutes=3, seconds=20),
                            likes=1, dislikes=2)
        Song.objects.create(name="in the end", singer="linkin park", duration=timedelta(minutes=3, seconds=36),
                            likes=5, dislikes=1)
        Song.objects.create(name="stairway to heaven", singer="led zeppelin", duration=timedelta(minutes=8, seconds=2),
                            likes=10, dislikes=0)

    def test_string_method(self):
        song1 = Song.objects.get(name="melodie")
        song2 = Song.objects.get(name="in the end")
        song3 = Song.objects.get(name="stairway to heaven")
        self.assertEqual(str(song1), "1. melodie by eu, 0:03:20 min,  Likes: 1, Dislikes: 2")
        self.assertEqual(str(song2), "2. in the end by linkin park, 0:03:36 min,  Likes: 5, Dislikes: 1")
        self.assertEqual(str(song3), "3. stairway to heaven by led zeppelin, 0:08:02 min,  Likes: 10, Dislikes: 0")

    def test_duration_in_minutes(self):
        song1 = Song.objects.get(name="melodie")
        song2 = Song.objects.get(name="in the end")
        song3 = Song.objects.get(name="stairway to heaven")
        self.assertAlmostEqual(song1.duration.total_seconds() / 60, 3.33, places=2)
        self.assertAlmostEqual(song2.duration.total_seconds() / 60, 3.60, places=2)
        self.assertAlmostEqual(song3.duration.total_seconds() / 60, 8.03, places=2)

    def test_likes_and_dislikes(self):
        song1 = Song.objects.get(name="melodie")
        song2 = Song.objects.get(name="in the end")
        song3 = Song.objects.get(name="stairway to heaven")
        self.assertEqual(song1.likes, 1)
        self.assertEqual(song1.dislikes, 2)
        self.assertEqual(song2.likes, 5)
        self.assertEqual(song2.dislikes, 1)
        self.assertEqual(song3.likes, 10)
        self.assertEqual(song3.dislikes, 0)

    def test_name_and_singer(self):
        song1 = Song.objects.get(name="melodie")
        song2 = Song.objects.get(singer="linkin park")
        song3 = Song.objects.get(name="stairway to heaven", singer="led zeppelin")
        self.assertEqual(song1.name, "melodie")
        self.assertEqual(song1.singer, "eu")
        self.assertEqual(song2.name, "in the end")
        self.assertEqual(song3.name, "stairway to heaven")
        self.assertEqual(song3.singer, "led zeppelin")