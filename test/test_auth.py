import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database import UserCRUD
from werkzeug.security import generate_password_hash
from database.models import User

import random

def random_user_data():
    rand = random.randint(1000, 9999)
    return {
        "name": "Test",
        "family": f"User{rand}",
        "phone": f"0905125{rand}",
        "username": f"testuser{rand}",
        "password": "secure123",
        "role": "employee",
        "national_id": f"123456{rand}"
    }

class PasswordResetTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

        db.create_all()

        # Save random user info for test access
        self.test_user_data = random_user_data()
        self.original_password = self.test_user_data['password']
        self.username = self.test_user_data['username']
        self.national_id = self.test_user_data['national_id']

        user = UserCRUD.create_user(**self.test_user_data)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_verify_and_reset_password(self):
        response = self.app.post('/api/verify-user', json={
            'username': self.username,
            'nationalId': self.national_id
        })
        self.assertEqual(response.status_code, 200)

        with self.app.session_transaction() as sess:
            self.assertEqual(sess['verified_user'], self.username)

        response = self.app.post('/api/reset-password', json={
            'newPassword': 'newsecurepassword'
        })
        self.assertEqual(response.status_code, 200)

        user = UserCRUD.get_user_by_username(username=self.username)
        self.assertTrue(user.check_password('newsecurepassword'))

    def test_verify_user_with_incorrect_info(self):
        response = self.app.post('/api/verify-user', json={
            'username': self.username,
            'nationalId': 'wrongnationalid'
        })
        self.assertEqual(response.status_code, 400)

        with self.app.session_transaction() as sess:
            self.assertNotIn('verified_user', sess)

    def test_reset_password_without_verification(self):
        # This should fail because session does not contain 'verified_user'
        response = self.app.post('/api/reset-password', json={
            'newPassword': 'newpassword123'
        })
        self.assertEqual(response.status_code, 400)

        user = UserCRUD.get_user_by_username(username=self.username)
        self.assertTrue(user.check_password(self.original_password))  # use the correct initial password


if __name__ == '__main__':
    unittest.main()
