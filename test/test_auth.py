import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database.models import User
from werkzeug.security import generate_password_hash

class PasswordResetTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

        db.create_all()

        user = User(username='testuser', national_id='1234567890')
        user.set_password('oldpassword')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_verify_and_reset_password(self):
        response = self.app.post('/api/verify-user', json={
            'username': 'testuser',
            'nationalId': '1234567890'
        })
        self.assertEqual(response.status_code, 200)

        with self.app.session_transaction() as sess:
            self.assertEqual(sess['verified_user'], 'testuser')

        response = self.app.post('/api/reset-password', json={
            'newPassword': 'newsecurepassword'
        })
        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(user.check_password('newsecurepassword'))

    def test_verify_user_with_incorrect_info(self):
        response = self.app.post('/api/verify-user', json={
            'username': 'testuser',
            'nationalId': 'wrongnationalid'
        })
        self.assertEqual(response.status_code, 400)

        with self.app.session_transaction() as sess:
            self.assertNotIn('verified_user', sess)

    def test_reset_password_without_verification(self):
        response = self.app.post('/api/reset-password', json={
            'newPassword': 'newpassword123'
        })
        self.assertEqual(response.status_code, 400)

        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(user.check_password('oldpassword'))


if __name__ == '__main__':
    unittest.main()
