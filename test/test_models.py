import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from database.models import User, db, bcrypt
from flask import Flask

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        # Create a Flask application context for testing
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        bcrypt.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_set_password(self):
        user = User(username='testuser', role='user')
        user.set_password('password123')
        self.assertTrue(user.password_hash is not None)
        self.assertTrue(bcrypt.check_password_hash(user.password_hash, 'password123'))

    def test_check_password(self):
        user = User(username='testuser', role='user')
        user.set_password('password123')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpassword'))

if __name__ == '__main__':
    unittest.main()