"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

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


def test(username, password, email, image_url):
    user = User.signup(email=email, password=password, username=username,
                       image_url=image_url)
    db.session.commit()


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
    def test_is_followed_by_true(self):
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()
        new_follow = Follows(user_following_id=self.user2.id,
                             user_being_followed_id=self.user1.id)
        db.session.add(new_follow)
        db.session.commit()
        self.assertEqual(self.user1.is_followed_by(self.user2), True)

    # **********
    # Does is_followed_by successfully detect when user1 is not followed by user2?
    # **********

    def test_is_followed_by_false(self):
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

        self.assertEqual(self.user1.is_followed_by(self.user2), False)

    # **********
    # Does User.create successfully create a new user given valid credentials?
    # **********

    def test_signup_user(self):
        user = User.signup(username='goofyguy123', password='thisisapassword321',
                           email='email_address@yahoo.com', image_url="https://lh3.googleusercontent.com/proxy/I9ot2AXlLZ83jGME-XGXpzvmjjusCrynU7FmBCzk_K_9b0vfOGll4Lwu437nWkyS7HyYlzHAZPgTcbhA5egPobaJlKq0J0Lvuyd3wpO-7K195eu4aclf")

        db.session.add(user)
        db.session.commit()

        self.assertTrue(user)
        self.assertEqual(user.username, 'goofyguy123')
        self.assertTrue(bcrypt.check_password_hash(
            user.password, 'thisisapassword321'))
        self.assertEqual(user.email, 'email_address@yahoo.com')
        self.assertEqual(
            user.image_url, "https://lh3.googleusercontent.com/proxy/I9ot2AXlLZ83jGME-XGXpzvmjjusCrynU7FmBCzk_K_9b0vfOGll4Lwu437nWkyS7HyYlzHAZPgTcbhA5egPobaJlKq0J0Lvuyd3wpO-7K195eu4aclf")

    # **********
    # Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
    # **********

    # NOT UNIQUE USERNAME
    # def test_signup_user_fail(self):
    #     db.session.add(self.user1)
    #     db.session.commit()

    #     self.assertRaises(IntegrityError, User.signup(username='username1', password='user1password', email='email1@gmail.com',
    #                                                   image_url="https://lh3.googleusercontent.com/proxy/I9ot2AXlLZ83jGME-XGXpzvmjjusCrynU7FmBCzk_K_9b0vfOGll4Lwu437nWkyS7HyYlzHAZPgTcbhA5egPobaJlKq0J0Lvuyd3wpO-7K195eu4aclf"))

    # **********
    # Does User.authenticate successfully return a user when given a valid username and password?
    # **********

    def test_authenticate_user_success(self):
        db.session.add(self.user1)
        db.session.commit()

        user = User.authenticate(
            self.user1.username, 'user1password')

        self.assertEqual(user, self.user1)
    # **********
    # Does User.authenticate fail to return a user when the username is invalid?
    # **********

    # **********
    # Does User.authenticate fail to return a user when the password is invalid?#
    # **********
