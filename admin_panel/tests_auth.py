from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User, PasswordResetToken
from django.conf import settings
from django.utils import timezone
from unittest.mock import patch, MagicMock
import uuid

class AdminAuthTests(APITestCase):
    def setUp(self):
        self.forgot_password_url = reverse('admin-forgot-password')
        self.set_new_password_url = reverse('admin-set-new-password')
        self.admin_email = "admin@test.com"
        self.admin_user = User.objects.create_superuser(
            email=self.admin_email,
            password="oldpassword123",
            name="Admin User"
        )

    @patch('sendgrid.SendGridAPIClient.send')
    def test_forgot_password_valid_email(self, mock_send):
        response = self.client.post(self.forgot_password_url, {"email": self.admin_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_send.called)
        self.assertTrue(PasswordResetToken.objects.filter(user=self.admin_user).exists())

    @patch('sendgrid.SendGridAPIClient.send')
    def test_forgot_password_invalid_email(self, mock_send):
        response = self.client.post(self.forgot_password_url, {"email": "wrong@email.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(mock_send.called)

    def test_set_new_password_valid_token(self):
        reset_token = PasswordResetToken.objects.create(user=self.admin_user)
        data = {
            "token": str(reset_token.token),
            "new_password": "newpassword123"
        }
        response = self.client.post(self.set_new_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.admin_user.refresh_from_db()
        self.assertTrue(self.admin_user.check_password("newpassword123"))
        
        reset_token.refresh_from_db()
        self.assertTrue(reset_token.is_used)

    def test_set_new_password_expired_token(self):
        reset_token = PasswordResetToken.objects.create(user=self.admin_user)
        # Manually expire the token by shifting created_at back
        PasswordResetToken.objects.filter(id=reset_token.id).update(
            created_at=timezone.now() - timezone.timedelta(minutes=20)
        )
        
        data = {
            "token": str(reset_token.token),
            "new_password": "newpassword123"
        }
        response = self.client.post(self.set_new_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("expired", str(response.data))

    def test_set_new_password_reused_token(self):
        reset_token = PasswordResetToken.objects.create(user=self.admin_user, is_used=True)
        data = {
            "token": str(reset_token.token),
            "new_password": "newpassword123"
        }
        response = self.client.post(self.set_new_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
