"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from models import db, connect_db, Message, User

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

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser1 = User.signup(username="testuser1",
                                     email="test1@test.com",
                                     password="testuser1",
                                     image_url=None)
        self.testuser2 = User.signup(username="testuser2",
                                     email="test2@test.com",
                                     password="testuser2",
                                     image_url=None)
        self.testuser1.id = id = 123
        self.testuser2.id = id = 321
        db.session.commit()

    def create_message(self):
        m = Message(id=332, text='This is a test message',
                    user_id=self.testuser1.id)
        db.session.add(m)
        db.session.commit()
        return m

    def test_add_message(self):
        """Can user add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new",
                          data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.filter(Message.text == 'Hello').first()
            print(
                f'************************ {msg} ************************')

            self.assertEqual(msg.text, "Hello")

    # ************************
    # Can user view a message?
    # ************************

    def test_show_message(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            message = self.create_message()

            resp = c.get(f'/messages/{message.id}')

            self.assertEquals(resp.status_code, 200)
            self.assertIn('This is a test message', str(resp.data))

    # ************************
    # When you’re logged in, can you delete a message as yourself?
    # ************************

    def test_delete_message(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            message = self.create_message()

            user = message.user
            resp = c.post(f'/messages/{message.id}/delete')

            self.assertEquals(resp.status_code, 302)
            self.assertNotIn(message, user.messages)

    # ************************
    # When you’re logged out, are you prohibited from adding messages?
    # ************************

    def test_unauthenticated_add_message(self):
        with self.client as c:

            resp = c.get("/messages/new",
                         data={"text": "Hello"}, follow_redirects=True)
            self.assertIn('Access unauthorized', str(resp.data))

    # ************************
    # When you’re logged out, are you prohibited from deleting messages?
    # ************************
    def test_unauthenticated_delete_message(self):
        message = self.create_message()
        user = message.user

        with self.client as c:

            resp = c.post(
                f'/messages/{message.id}/delete', follow_redirects=True)

            self.assertIn('Access unauthorized', str(resp.data))

    # ************************
    # When you’re logged in, are you prohibiting from deleting a message as another user?
    # ************************
    def test_unauthorized_delete_message(self):
        message = self.create_message()
        user = message.user

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser2.id

            resp = c.post(
                f"/messages/{message.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                "Access unauthorized - you are attempting to delete the post of another user", str(resp.data))
