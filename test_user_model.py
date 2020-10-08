"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.user1 = User(email='email1@gmail.com', password='user1password', username='username1',
                          bio='This is the bio for user1')
        self.user2 = User(email='email2@gmail.com', password='user2password', username='username2',
                          bio='This is the bio for user2')
        self.user3 = User(email='email3@gmail.com', password='user3password', username='username3',
                          bio='This is the bio for user3')
        self.user4 = User(email='email4@gmail.com', password='user4password', username='username4',
                          bio='This is the bio for user4')
        self.user5 = User(email='email5@gmail.com', password='user5password', username='username5',
                          bio='This is the bio for user5')

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    # **********
    # Does the repr method work as expected?
    # **********

    def test_user_model_repr(self):
        """Does basic model work?"""
        db.session.add(self.user1)
        db.session.commit()
        # User should have no messages & no followers
        self.assertEqual(
            f'{self.user1}', f'<User #{self.user1.id}: username1, email1@gmail.com>')

    # **********
    # Does is_following successfully detect when user1 is following user2?
    # **********
    def test_is_following_true(self):
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()
        new_follow = Follows(user_following_id=self.user1.id,
                             user_being_followed_id=self.user2.id)
        db.session.add(new_follow)
        db.session.commit()
        self.assertEqual(self.user1.is_following(self.user2), True)

    # **********
    # Does is_following successfully detect when user1 is not following user2?
    # **********
    def test_is_following_false(self):
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

        self.assertEqual(self.user1.is_following(self.user2), False)
    # **********
    # Does is_followed_by successfully detect when user1 is followed by user2?
    # **********

    # **********
    # Does is_followed_by successfully detect when user1 is not followed by user2?
    # **********

    # **********
    # Does User.create successfully create a new user given valid credentials?
    # **********

    # **********
    # Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
    # **********

    # **********
    # Does User.authenticate successfully return a user when given a valid username and password?
    # **********

    # **********
    # Does User.authenticate fail to return a user when the username is invalid?
    # **********

    # **********
    # Does User.authenticate fail to return a user when the password is invalid?#
    # **********
