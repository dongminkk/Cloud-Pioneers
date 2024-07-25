from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import json

class ReviewTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Test user setup
        self.test_user_nickname = 'testuser'
        self.test_user_id = 1  # This should correspond to the ID in your test database

        # URLs
        self.post_review_url = reverse('post_review', kwargs={'video_id': 1})
        self.get_all_review_url = reverse('get_all_review')
        self.get_review_url = reverse('get_review', kwargs={'video_id': 1})
        self.delete_review_url = reverse('delete_review', kwargs={'video_id': 1, 'review_id': 1})
        self.put_review_url = reverse('update_review', kwargs={'video_id': 1, 'review_id': 1})

    #리뷰 생성 테스트
    @patch('mysql.connector.connect')
    def test_post_review_success(self, mock_connect):
        # Mocking database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (self.test_user_id,)
        
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = []

        # Test data
        data = {
            'video_id': 1,
            'rating': 5,
            'comments': 'reviews 앱 테스트 코드 결과',
            'nickname': self.test_user_nickname
        }

        response = self.client.post(self.post_review_url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()[0]['video_id'], data['video_id'])
        self.assertEqual(response.json()[0]['rating'], data['rating'])
        self.assertEqual(response.json()[0]['comments'], data['comments'])
        self.assertEqual(response.json()[0]['nickname'], data['nickname'])


    #모든 리뷰 조회 테스트
    @patch('mysql.connector.connect')
    def test_get_all_review_success(self, mock_connect):
        # Mocking database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'review_id': 1, 'rating': 5, 'comments': 'Great video!', 'users_id': self.test_user_id, 'video_id': 1},
            {'review_id': 2, 'rating': 4, 'comments': 'Good video!', 'users_id': self.test_user_id, 'video_id': 1}
        ]

        response = self.client.get(self.get_all_review_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['rating'], 5)


    #특정 비디오에 대한 리뷰 조회 테스트
    @patch('mysql.connector.connect')
    def test_get_review_success(self, mock_connect):
        # Mocking database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'review_id': 1, 'rating': 5, 'comments': 'Great video!', 'nickname': self.test_user_nickname}
        ]

        response = self.client.get(self.get_review_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['rating'], 5)


    #리뷰 삭제 테스트
    @patch('mysql.connector.connect')
    def test_delete_review_success(self, mock_connect):
        # Mocking database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (self.test_user_id,)
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = []

        data = {'user_name': self.test_user_nickname}
        response = self.client.delete(self.delete_review_url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json()[0]['message'], 'Review deleted successfully')


    #리뷰 수정 테스트
    @patch('mysql.connector.connect')
    def test_put_review_success(self, mock_connect):
        # Mocking database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (self.test_user_id,)
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = []

        data = {
            'user_name': self.test_user_nickname,
            'new_rating': 4,
            'new_comment': 'Updated comment!'
        }
        response = self.client.put(self.put_review_url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['message'], 'Review updated successfully')
        self.assertEqual(response.json()[0]['review']['new_comment'], 'Updated comment!')

