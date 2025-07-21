# test_api.py

import unittest
import sys
sys.path.append('..')
from app import app, TimelinePost
from peewee import SqliteDatabase

# Use SQLite in-memory for testing
test_db = SqliteDatabase(':memory:')
MODELS = [TimelinePost]

class TestTimelineAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Bind and initialize in-memory DB
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_post_and_get_timeline_posts(self):
        post_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "content": "Testing the timeline API!"
        }

        # Create post via API
        response = self.client.post("/api/timeline_post", data=post_data)
        self.assertEqual(response.status_code, 201)
        json_response = response.get_json()
        post_id = json_response["id"]
        self.assertIsNotNone(post_id)

        # Fetch all posts and ensure the new post is included
        response_all = self.client.get("/api/timeline_post")
        self.assertEqual(response_all.status_code, 200)
        posts = response_all.get_json()["timeline_posts"]
        self.assertTrue(any(p["id"] == post_id for p in posts))

        # Fetch the specific post by ID
        response_one = self.client.get(f"/api/timeline_post/{post_id}")
        self.assertEqual(response_one.status_code, 200)
        fetched_post = response_one.get_json()
        self.assertEqual(fetched_post["name"], post_data["name"])
        self.assertEqual(fetched_post["email"], post_data["email"])
        self.assertEqual(fetched_post["content"], post_data["content"])

if __name__ == '__main__':
    unittest.main()
