from django.test import TestCase
from .models import User


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        User.objects.create(email='hamat.ibrahim3@gmail.com', name='ibrahim hamzat')
        User.objects.create(email="admin@ymail.com", name='ibrahim')

    def test_user_can_register(self):
        """User can create account testing """
        user1 = User.objects.get(name="ibrahim hamzat")
        user2 = User.objects.get(name="ibrahim")
        self.assertEqual(user1.email, 'hamat.ibrahim3@gmail.com')
        self.assertEqual(user2.email, 'admin@ymail.com')

    def test_user_can_login(self):
        pass
