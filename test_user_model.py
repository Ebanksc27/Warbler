"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

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

class UserModelTestCase(TestCase):
    """Tests for User model."""

    def setUp(self):
        """Create test client and sample data."""
        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        db.session.commit()

    def test_user_repr(self):
        """Does the repr method work as expected?"""
        self.assertEqual(repr(self.testuser), f"<User #{self.testuser.id}: {self.testuser.username}, {self.testuser.email}>")

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2 and not following user2?"""
        user2 = User.signup(username="testuser2", email="test2@test.com", password="testuser2", image_url=None)
        db.session.commit()

        self.testuser.following.append(user2)
        db.session.commit()

        self.assertTrue(self.testuser.is_following(user2))
        self.assertFalse(user2.is_following(self.testuser))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2 and not followed by user2?"""
        user2 = User.signup(username="testuser2", email="test2@test.com", password="testuser2", image_url=None)
        db.session.commit()

        user2.following.append(self.testuser)
        db.session.commit()

        self.assertTrue(self.testuser.is_followed_by(user2))
        self.assertFalse(user2.is_followed_by(self.testuser))

    def test_user_create(self):
        """Does User.create successfully create a new user given valid credentials and fail with invalid data?"""
        user = User.signup(username="newuser", email="new@user.com", password="newpassword", image_url=None)
        db.session.commit()

        found_user = User.query.filter_by(username="newuser").first()
        self.assertIsNotNone(found_user)

        with self.assertRaises(ValueError):
            invalid_user = User.signup(username=None, email=None, password="password", image_url=None)

    def test_user_authenticate(self):
        """Does User.authenticate successfully return a user with valid credentials and fail with invalid data?"""
        user = User.authenticate(self.testuser.username, "testuser")
        self.assertEqual(user.id, self.testuser.id)

        self.assertFalse(User.authenticate("invalidusername", "testuser"))
        self.assertFalse(User.authenticate(self.testuser.username, "invalidpassword"))
