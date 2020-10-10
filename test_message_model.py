from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from models import db, User, Message, Follows, bcrypt
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.user1 = User.signup(email='email1@gmail.com', password='user1password', username='username1',
                                 image_url=None)
        self.user2 = User.signup(email='email2@gmail.com', password='user2password', username='username2',
                                 image_url=None)

        self.user1.id = 789
        self.user2.id = 987

        db.session.commit()

    # Does basic model work?
    def test_create_message(self):
        msg = Message(text="This is a test message", user_id=self.user1.id)
        msg.id = 123

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(msg.text, 'This is a test message')
        self.assertEqual(msg.id, 123)
        self.assertEqual(msg.user_id, 789)
        self.assertIsInstance(msg.timestamp, datetime)

    # Does user_id correspond to the correct / signed in user?
    def test_correct_user_id(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            msg = Message(text="This is a test message",
                          user_id=sess[CURR_USER_KEY])
            msg.id = 456

            db.session.add(msg)
            db.session.commit()

            self.assertEqual(msg.user_id, 789)
    # Does message.user function correctly?

    def test_user_relationship(self):
        msg = Message(text="This is a test message", user_id=self.user1.id)
        msg.id = 567

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(msg.user, self.user1)
        self.assertIn(msg, self.user1.messages)
