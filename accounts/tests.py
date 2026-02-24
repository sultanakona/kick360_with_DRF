from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User
from access_codes.models import AccessCode
from unittest.mock import patch

class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        
    @patch('accounts.serializers.ShopifyService.verify_access_code')
    def test_successful_registration(self, mock_verify):
        mock_verify.return_value = {'is_valid': True, 'meta': {'mocked': True}}
        
        data = {
            "name": "Test User",
            "country": "Germany",
            "position": "Forward",
            "access_code": "VALID_CODE"
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(AccessCode.objects.filter(code="VALID_CODE", is_consumed=True).exists())

    @patch('accounts.serializers.ShopifyService.verify_access_code')
    def test_registration_invalid_code(self, mock_verify):
        mock_verify.return_value = {'is_valid': False, 'meta': {}}
        
        data = {
            "name": "Test User",
            "country": "Germany",
            "position": "Forward",
            "access_code": "INVALID_CODE"
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(User.objects.count(), 0)

    @patch('accounts.serializers.ShopifyService.verify_access_code')
    def test_registration_already_consumed_code(self, mock_verify):
        mock_verify.return_value = {'is_valid': True, 'meta': {}}
        AccessCode.objects.create(code="CONSUMED_CODE", is_consumed=True) # Already consumed locally
        
        data = {
            "name": "Test User",
            "country": "Germany",
            "position": "Forward",
            "access_code": "CONSUMED_CODE"
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_successful_login(self):
        # Create active user
        User.objects.create_user(access_code="LOGIN_CODE", name="Log User")
        
        data = {
            "access_code": "LOGIN_CODE"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data']['tokens'])

    def test_login_invalid_code(self):
        data = {
            "access_code": "UNKNOWN_CODE"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
