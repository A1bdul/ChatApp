from django.test import TestCase
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase
import getpass

from sqlparse import format


# Create your tests here.

class EmailTest(APITestCase):
    register_url = '/api/v1/users/'

    user_data = {
        'email': 'abdc@gmail.com',
        'username': 'A1bdl',
        'password': '123456789'
    }

    def test_register_with_email(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
