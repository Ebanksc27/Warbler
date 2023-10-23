import os
from unittest import TestCase
from models import db, User, Message

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Test methods for Message model."""

    def setUp(self):
        """Create test client, add sample data."""
        Message.query.delete()
        User.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()
