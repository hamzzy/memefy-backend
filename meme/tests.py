from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import CustomUser

from rest_framework.test import APIClient


class MemeCatTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.data = {
            "name": "funny",
            "slug": "funny"

        }

    def test_cat_create(self):
        """ Testing CustomUser Registration"""
        response = self.client.post(reverse('meme_cat'), data=self.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_get_cat(self):
        """ Testing CustomUser AUTH """
        response = self.client.get(reverse('meme_cat'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
