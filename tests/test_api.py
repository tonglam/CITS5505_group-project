"""Tests for the API module."""

from flask import Flask
from flask.testing import FlaskClient

from app.constants import HttpRequestEnum
from app.extensions import db
from app.models.category import Category
from app.models.reply import Reply
from app.models.request import Request
from app.models.tag import Tag
from app.models.user import User
from app.models.user_like import UserLike
from app.models.user_notice import UserNotice, UserNoticeModuleEnum
from app.models.user_record import UserRecord
from app.models.user_save import UserSave
from tests.config import AuthActions, TestBase

_PREFIX = "/api/v1"


class TestApi(TestBase):
    """This class contains the test cases for the API module."""

    def test_get_user_posts(self, app: Flask, client: FlaskClient):
        """Test the user posts API."""

        url = _PREFIX + "/users/posts"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_posts_count = Request.query.filter_by(author_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_posts"]), min(user_posts_count, 10)
        )

    def test_get_user_replies(self, app: Flask, client: FlaskClient):
        """Test the user replies API."""

        url = _PREFIX + "/users/replies"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_replies_count = Reply.query.filter_by(replier_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_replies"]), min(user_replies_count, 10)
        )

        # logout
        auth.logout()

    def test_get_user_records(self, app: Flask, client: FlaskClient):
        """Test the user records GET API."""

        url = _PREFIX + "/users/records"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_records_count = UserRecord.query.filter_by(user_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_records"]), min(user_records_count, 10)
        )

        # logout
        auth.logout()

    def test_post_user_record(self, app: Flask, client: FlaskClient):
        """Test POST the user record API."""

        url = _PREFIX + "/users/records/%s"

        user = None
        user_records_ids = []
        request_ids = []
        with app.app_context():
            user = User.query.first()
            user_records_ids = [
                record.request_id
                for record in UserRecord.query.filter_by(user_id=user.id).all()
            ]
            request_ids = [request.id for request in Request.query.all()]

        request_id = [
            request_id
            for request_id in request_ids
            if request_id not in user_records_ids
        ][0]

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # test valid record
        response = client.post(url % request_id, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.CREATED.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.CREATED.value)

        user_record = UserRecord.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNotNone(user_record)

        # test invalid request_id
        response = client.post(url % 9999999, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # test existing record
        response = client.post(url % request_id, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.BAD_REQUEST.value)

        # logout
        auth.logout()

    def test_delete_user_record(self, app: Flask, client: FlaskClient):
        """Test DELETE the user record API."""

        url = _PREFIX + "/users/records/%s"

        user_record = None
        user = None
        with app.app_context():
            user_record = UserRecord.query.first()
            user = User.query.filter_by(id=user_record.user_id).first()

        request_id = user_record.request_id

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # test valid unlike
        response = client.delete(url % request_id, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.NO_CONTENT.value)

        user_record = UserRecord.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()

        # logout
        auth.logout()

    def test_get_user_likes(self, app: Flask, client: FlaskClient):
        """Test the user likes API."""

        url = _PREFIX + "/users/likes"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_likes_count = UserLike.query.filter_by(user_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_likes"]), min(user_likes_count, 10)
        )

        # logout
        auth.logout()

    def test_post_user_like(self, app: Flask, client: FlaskClient):
        """Test POST the user like API."""

        url = _PREFIX + "/users/likes"

        user = None
        user_likes_ids = []
        request_ids = []
        with app.app_context():
            user = User.query.first()
            user_likes_ids = [
                like.request_id
                for like in UserLike.query.filter_by(user_id=user.id).all()
            ]
            request_ids = [request.id for request in Request.query.all()]

        request_id = [
            request_id for request_id in request_ids if request_id not in user_likes_ids
        ][0]

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # test valid like
        response = client.post(
            url, json={"request_id": request_id}, headers=auth.get_auth_headers()
        )
        self.assertEqual(response.status_code, HttpRequestEnum.CREATED.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.CREATED.value)

        user_like = UserLike.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNotNone(user_like)

        # test invalid request_id
        response = client.post(
            url, json={"request_id": 9999999}, headers=auth.get_auth_headers()
        )
        self.assertEqual(response.status_code, HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # test existing like
        response = client.post(
            url, json={"request_id": request_id}, headers=auth.get_auth_headers()
        )
        self.assertEqual(response.status_code, HttpRequestEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.BAD_REQUEST.value)

        # logout
        auth.logout()

    def test_get_user_saves(self, app: Flask, client: FlaskClient):
        """Test the user saves API."""

        url = _PREFIX + "/users/saves"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_saves_count = UserSave.query.filter_by(user_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_saves"]), min(user_saves_count, 10)
        )

        # logout
        auth.logout()

    def test_post_user_save(self, app: Flask, client: FlaskClient):
        """Test POST the user save API."""

        url = _PREFIX + "/users/saves"

        user = None
        user_saves_ids = []
        request_ids = []
        with app.app_context():
            user = User.query.first()
            user_saves_ids = [
                save.request_id
                for save in UserSave.query.filter_by(user_id=user.id).all()
            ]
            request_ids = [request.id for request in Request.query.all()]

        request_id = [
            request_id for request_id in request_ids if request_id not in user_saves_ids
        ][0]

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # test valid save
        response = client.post(
            url, json={"request_id": request_id}, headers=auth.get_auth_headers()
        )
        self.assertEqual(response.status_code, HttpRequestEnum.CREATED.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.CREATED.value)

        user_save = UserSave.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNotNone(user_save)

        # test invalid request_id
        response = client.post(
            url, json={"request_id": 9999999}, headers=auth.get_auth_headers()
        )
        self.assertEqual(response.status_code, HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # test existing save
        response = client.post(
            url, json={"request_id": request_id}, headers=auth.get_auth_headers()
        )
        self.assertEqual(response.status_code, HttpRequestEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.BAD_REQUEST.value)

        # logout
        auth.logout()

    def test_get_user_notifications(self, app: Flask, client: FlaskClient):
        """Test the user notifications GET API."""

        url = _PREFIX + "/users/notifications"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_notifications_count = UserNotice.query.filter_by(user_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_notifications"]),
            min(user_notifications_count, 10),
        )

        # logout
        auth.logout()

    def test_get_user_notification(self, app: Flask, client: FlaskClient):
        """Test the user notification GET API."""

        url = _PREFIX + "/users/notifications/%s"
        user_email = None
        notification_id = None

        with app.app_context():
            user = User.query.first()
            user_email = user.email  # Store email instead of user object
            # Create a test notification if none exists
            user_notification = UserNotice.query.filter_by(user_id=user.id).first()
            if not user_notification:
                user_notification = UserNotice(
                    user_id=user.id,
                    subject="Test Notification",
                    content="Test Content",
                    module=UserNoticeModuleEnum.COMMUNITY.value,
                    status=False,
                )
                db.session.add(user_notification)
                db.session.commit()
            notification_id = user_notification.id

        # login
        auth = AuthActions(client)
        auth.login(email=user_email, password="Password@123")

        # check valid data
        response = client.get(url % notification_id, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # test invalid notification_id
        response = client.get(url % 9999999, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # logout
        auth.logout()

    def test_put_user_notification(self, app: Flask, client: FlaskClient):
        """Test the user notification PUT API."""

        url = _PREFIX + "/users/notifications/%s"

        user = None
        user_notification = None
        with app.app_context():
            user = User.query.first()
            user_notification = UserNotice.query.filter_by(user_id=user.id).first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # test valid notification update
        response = client.put(
            url % user_notification.id, headers=auth.get_auth_headers()
        )
        self.assertEqual(response.status_code, HttpRequestEnum.NO_CONTENT.value)

        # For NO_CONTENT responses, there is no response body to check

        # test invalid notification_id
        response = client.put(url % 9999999, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # logout
        auth.logout()

    def test_get_user_stat(self, app: Flask, client: FlaskClient):
        """Test the user stat GET API."""

        url = _PREFIX + "/users/stats"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # logout
        auth.logout()

    def test_get_categories(self, app: Flask, client: FlaskClient):
        """Test the categories GET API."""

        url = _PREFIX + "/categories"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        categories_count = Category.query.count()
        self.assertEqual(
            len(response_data["data"]["categories"]), min(categories_count, 10)
        )

        # logout
        auth.logout()

    def test_get_category(self, app: Flask, client: FlaskClient):
        """Test the category GET API."""

        url = _PREFIX + "/categories/%s"

        user = None
        category = None
        with app.app_context():
            user = User.query.first()
            category = Category.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url % category.id, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # test invalid category_id
        response = client.get(url % 9999999, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # logout
        auth.logout()

    def test_get_tags(self, app: Flask, client: FlaskClient):
        """Test the tags GET API."""

        url = _PREFIX + "/tags"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        tags_count = Tag.query.count()
        self.assertEqual(len(response_data["data"]["tags"]), min(tags_count, 10))

        # logout
        auth.logout()

    def test_get_tag(self, app: Flask, client: FlaskClient):
        """Test the tag GET API."""

        url = _PREFIX + "/tags/%s"

        user = None
        tag = None
        with app.app_context():
            user = User.query.first()
            tag = Tag.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url % tag.id, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # test invalid tag_id
        response = client.get(url % 9999999, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # logout
        auth.logout()

    def test_get_stats(self, app: Flask, client: FlaskClient):
        """Test the stats GET API."""

        url = _PREFIX + "/stats"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        auth = AuthActions(client)
        auth.login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url, headers=auth.get_auth_headers())
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # logout
        auth.logout()
