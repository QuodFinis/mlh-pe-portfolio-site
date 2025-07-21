import unittest
import os
import sys
from datetime import datetime

sys.path.append('..')
os.environ['TESTING'] = 'true'

from app import app, TimelinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page_title(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<title>Mahmud Hasan</title>', html)

    def test_about_me_section(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check section header exists
        self.assertIn('<h2 class="mb-4">About Me</h2>', html)
        # Check at least one paragraph exists in the about section
        self.assertIn('<div class="about-card">', html)
        self.assertIn('<p class="mb-3">', html)

    def test_work_experience_section(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check section header exists
        self.assertIn('<h2 class="mb-4">Work Experience</h2>', html)
        # Check at least one job listing exists
        self.assertIn('<div class="work-card mb-4">', html)
        self.assertIn('<h3>', html)  # Job title
        self.assertIn('<ul class="mt-3">', html)  # Description list

    def test_hobbies_section(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check section header exists
        self.assertIn('<h2 class="mb-4">Hobbies</h2>', html)
        # Check hobbies grid and at least one hobby card exists
        self.assertIn('<div class="hobbies-grid">', html)
        self.assertIn('<div class="hobby-card">', html)
        # Check hobby image and name are present
        self.assertIn('img/', html)  # Checking for image path
        self.assertIn('<p class="mt-3">', html)  # Hobby name

    def test_timeline_api(self):
        response = self.client.get('/api/timeline_post')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        json_data = response.get_json()
        self.assertIn('timeline_posts', json_data)
        self.assertEqual(len(json_data['timeline_posts']), 0)

    def test_timeline_form_submission(self):
        """Test form submission creates a new timeline post"""
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'content': 'This is a test post'
        }
        response = self.client.post('/submit_timeline_post', data=test_data)
        self.assertEqual(response.status_code, 302)  # Check redirect after POST
        self.assertIn('/timeline', response.location)

        # Verify post appears in the timeline
        timeline_response = self.client.get('/timeline')
        html = timeline_response.get_data(as_text=True)
        self.assertIn(test_data['name'], html)
        self.assertIn(test_data['content'], html)

    def test_timeline_api_post(self):
        """Test API endpoint for creating timeline posts"""
        test_data = {
            'name': 'API Test User',
            'email': 'api@example.com',
            'content': 'API test content'
        }
        response = self.client.post('/api/timeline_post', data=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.is_json)
        json_data = response.get_json()
        self.assertIn('id', json_data)
        self.assertEqual(json_data['message'], "Resource created successfully.")

    def test_timeline_api_get_single_post(self):
        """Test API endpoint for retrieving a single post"""
        # First create a test post
        test_post = TimelinePost.create(
            name='Single Post Test',
            email='single@test.com',
            content='Test content for single post'
        )

        # Then retrieve it
        response = self.client.get(f'/api/timeline_post/{test_post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        post_data = response.get_json()
        self.assertEqual(post_data['name'], 'Single Post Test')
        self.assertEqual(post_data['content'], 'Test content for single post')

    def test_malformed_timeline_post(self):
        """Test API with malformed data"""
        # Missing name
        response = self.client.post('/api/timeline_post', data={
            'email': 'john@example.com',
            'content': 'This post has no name'
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.is_json)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "Invalid Name")

        # Empty content
        response = self.client.post('/api/timeline_post', data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.is_json)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "Invalid Content")

        # Malformed email
        response = self.client.post('/api/timeline_post', data={
            'name': 'John Doe',
            'email': 'not-an-email',
            'content': 'This post has a malformed email'
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.is_json)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "Invalid Email")