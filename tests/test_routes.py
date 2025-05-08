# tests/test_routes.py
import unittest
from app import create_app
from app.models import db, User, Todo
from flask import json
import os

class TodoApiTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            user = User(email="test@example.com")
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def auth_header(self):
        return {"Authorization": f"Bearer {self.user_id}"}

    def test_create_todo(self):
        res = self.client.post("/todos", json={
            "title": "Test Todo",
            "description": "Testing create"
        }, headers=self.auth_header())
        self.assertEqual(res.status_code, 201)
        self.assertIn("Test Todo", res.get_data(as_text=True))

    def test_list_todos(self):
        self.client.post("/todos", json={
            "title": "List Me",
            "description": "desc"
        }, headers=self.auth_header())
        res = self.client.get("/todos", headers=self.auth_header())
        self.assertEqual(res.status_code, 200)
        self.assertIn("List Me", res.get_data(as_text=True))

    def test_mark_todo_complete(self):
        create = self.client.post("/todos", json={
            "title": "Complete Me",
            "description": "in test"
        }, headers=self.auth_header())
        todo_id = json.loads(create.data)["id"]

        res = self.client.put(f"/todos/{todo_id}/complete", headers=self.auth_header())
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(data["completed"])

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
