from unittest import TestCase
from app import app
from utils import db, connect_db


# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookyourservices_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskTests(TestCase):
    """Test class for home blueprint"""

    def setUp(self):
        """Clean up any exists users and add a new user"""

        user = User(first_name="AAA", last_name="BBB", image_url="sample_url")
        db.session.add(user)
        db.session.commit()

        post = Post(user_id=user.id, title="test title",
                    content="test content")
        db.session.add(post)
        db.session.commit()

        tag = Tag(name="tag test")
        db.session.add(tag)
        db.session.commit()

        post.tags.append(tag)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_users(self):
        """Testing the all users page"""
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("AAA BBB", html)