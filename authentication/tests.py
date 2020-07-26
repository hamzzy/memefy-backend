from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import CustomUser

from rest_framework.test import APIClient


class UserTest(TestCase):

    def setUp(self):
        CustomUser.objects.create(email='hamat.ibrahim3@gmail.com', name='ibrahim hamzat')
        CustomUser.objects.create(email="admin@ymail.com", name='ibrahim')
        self.client = APIClient()
        self.data = {
            "email": "gjgktg.ibrahim3@gmail.com",
            "name": "ibrahim Hamzat",
            "password": "hamzat123"
        }

    # def test_user_db(self):
    #     """CustomUser can create account testing """
    #     user1 = CustomUser.objects.get(name="ibrahim hamzat")
    #     user2 = CustomUser.objects.get(name="ibrahim")
    #     self.assertEqual(user1.email, 'hamat.ibrahim3@gmail.com')
    #     self.assertEqual(user2.email, 'admin@ymail.com')

    def test_user_can_register(self):
        """ Testing CustomUser Registration"""
        response = self.client.post(reverse('sign_up'), data=self.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['msg'], 'CustomUser Registered')

    def test_user_can_login(self):
        """ Testing CustomUser AUTH """
        response = self.client.post(reverse('sign_in'),data={})
