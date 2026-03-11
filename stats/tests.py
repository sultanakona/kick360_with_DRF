from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from follows.models import Follow

class LeaderboardTests(APITestCase):
    def setUp(self):
        # Create a few users with different points and countries
        # Use 8-character access_code to bypass subscription check (see User.is_subscription_active)
        self.user1 = User.objects.create_user(email="user1@example.com", name="User 1")
        self.user1.access_code = "ABCDEFGH"
        self.user1.points = 1000
        self.user1.country = "Germany"
        self.user1.save()
        
        self.user2 = User.objects.create_user(email="user2@example.com", name="User 2")
        self.user2.points = 2000
        self.user2.country = "France"
        self.user2.save()
        
        self.user3 = User.objects.create_user(email="user3@example.com", name="User 3")
        self.user3.points = 1500
        self.user3.country = "Germany"
        self.user3.save()
        
        # Create more users to test the 11-player limit
        for i in range(4, 15):
            User.objects.create_user(email=f"user{i}@example.com", name=f"User {i}", points=500 + i, country="Germany" if i % 2 == 0 else "USA")
            
        self.client.force_authenticate(user=self.user1)
        self.url = reverse('stats-leaderboard')

    def test_leaderboard_everyone(self):
        """Test getting top 11 players from everyone"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        top_11 = response.data['data']['top_11']
        self.assertEqual(len(top_11), 11)
        
        # Check sorting: User 2 (2000 pts) should be first, User 3 (1500) second, User 1 (1000) third
        self.assertEqual(top_11[0]['name'], "User 2")
        self.assertEqual(top_11[1]['name'], "User 3")
        self.assertEqual(top_11[2]['name'], "User 1")
        self.assertEqual(top_11[0]['points'], 2000)
        self.assertEqual(top_11[0]['rank'], 1)

    def test_leaderboard_germany(self):
        """Test getting top players from Germany"""
        response = self.client.get(self.url, {'filter': 'germany'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        top_11 = response.data['data']['top_11']
        for p in top_11:
            # We need to verify that all returned users are from Germany
            user = User.objects.get(id=p['id'])
            self.assertEqual(user.country.lower(), "germany")

    def test_leaderboard_following(self):
        """Test getting top players from following list"""
        # user1 follows user2
        Follow.objects.create(follower=self.user1, following=self.user2)
        
        response = self.client.get(self.url, {'filter': 'following'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        top_11 = response.data['data']['top_11']
        # Should only contain user2
        self.assertEqual(len(top_11), 1)
        self.assertEqual(top_11[0]['name'], "User 2")

    def test_leaderboard_response_structure(self):
        """Verify the response structure matches requirements"""
        response = self.client.get(self.url)
        self.assertIn('success', response.data)
        self.assertIn('data', response.data)
        self.assertIn('top_11', response.data['data'])
        
        first_player = response.data['data']['top_11'][0]
        required_fields = ['id', 'name', 'avatar', 'points', 'rank', 'total_kicks', 'streak']
        for field in required_fields:
            self.assertIn(field, first_player)
