"""Tests for the API module."""

from flask import Flask
from flask.testing import FlaskClient

from app.constants import HttpRequestEnum
from app.models.category import Category
from app.models.reply import Reply
from app.models.request import Request
from app.models.tag import Tag
from app.models.user import User
from app.models.user_like import UserLike
from app.models.user_notice import UserNotice
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord
from app.models.user_save import UserSave
from tests.config import AuthActions, TestBase

_PREFIX = "/api/v1"


class TestApi(TestBase):
    """This class contains the test cases for the API module."""

    def test_get_user_communities(self, app: Flask, client: FlaskClient):
        """Test the user communities API."""

        url = _PREFIX + "/users/communities"

        user_preference = None
        user = None
        with app.app_context():
            user_preference = UserPreference.query.first()
            user = User.query.filter_by(id=user_preference.user_id).first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        community_ids = [
            int(id.strip()) for id in user_preference.communities.strip("[]").split(",")
        ]
        self.assertEqual(
            len(response_data["data"]["user_communities"]),
            min(len(community_ids), 10),
        )

        # logout
        AuthActions(client).logout()

    def test_get_user_posts(self, app: Flask, client: FlaskClient):
        """Test the user posts API."""

        url = _PREFIX + "/users/posts"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
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
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_replies_count = Reply.query.filter_by(replier_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_replies"]), min(user_replies_count, 10)
        )

        # logout
        AuthActions(client).logout()

    def test_get_user_records(self, app: Flask, client: FlaskClient):
        """Test the user records GET API."""

        url = _PREFIX + "/users/records"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_records_count = UserRecord.query.filter_by(user_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_records"]), min(user_records_count, 10)
        )

        # logout
        AuthActions(client).logout()

    def test_post_user_record(self, app: Flask, client: FlaskClient):
        """Test POST the user record API."""

        url = _PREFIX + "/users/records/%s"

        user = None
        request = None
        with app.app_context():
            user = User.query.first()
            request = Request.query.first()

        request_id = request.id

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # test valid like
        response = client.post(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.CREATED.value)

        user_record = UserRecord.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNotNone(user_record)

        # test invalid request_id
        response = client.post(url % 9999999)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # test existing like
        response = client.post(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.BAD_REQUEST.value)

        # logout
        AuthActions(client).logout()

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
        AuthActions(client).login(email=user.email, password="Password@123")

        # test valid unlike
        response = client.delete(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.NO_CONTENT.value)

        user_record = UserRecord.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()

        # logout
        AuthActions(client).logout()

    def test_get_user_likes(self, app: Flask, client: FlaskClient):
        """Test the user likes API."""

        url = _PREFIX + "/users/likes"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        user_likes_count = UserLike.query.filter_by(user_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_likes"]), min(user_likes_count, 10)
        )

        # logout
        AuthActions(client).logout()

    def test_post_user_like(self, app: Flask, client: FlaskClient):
        """Test POST the user like API."""

        url = _PREFIX + "/users/likes/%s"

        user = None
        request = None
        with app.app_context():
            user = User.query.first()
            request = Request.query.first()

        request_id = request.id

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # test valid like
        response = client.post(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.CREATED.value)

        user_like = UserLike.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNotNone(user_like)

        # test invalid request_id
        response = client.post(url % 9999999)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # test existing like
        response = client.post(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.BAD_REQUEST.value)

        # logout
        AuthActions(client).logout()

    def test_delete_user_like(self, app: Flask, client: FlaskClient):
        """Test DELETE the user like API."""

        url = _PREFIX + "/users/likes/%s"

        user_like = None
        user = None
        with app.app_context():
            user_like = UserLike.query.first()
            user = User.query.filter_by(id=user_like.user_id).first()

        request_id = user_like.request_id

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # test valid unlike
        response = client.delete(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.NO_CONTENT.value)

        user_like = UserLike.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNone(user_like)

        # test invalid request_id
        response = client.delete(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_saves(self, app: Flask, client: FlaskClient):
        """Test the user saves API."""

        url = _PREFIX + "/users/saves"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.CREATED.value)

        user_saves_count = UserSave.query.filter_by(user_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_saves"]), min(user_saves_count, 10)
        )

        # logout
        AuthActions(client).logout()

    def test_post_user_save(self, app: Flask, client: FlaskClient):
        """Test POST the user save API."""

        url = _PREFIX + "/users/saves/%s"

        user = None
        request = None
        with app.app_context():
            user = User.query.first()
            request = Request.query.filter_by(author_id=user.id).first()

        request_id = request.id

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # test valid save
        response = client.post(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.CREATED.value)
        self.assertEqual(response_data["message"], "save success")

        user_save = UserSave.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNotNone(user_save)

        # test invalid request_id
        response = client.post(url % 9999999)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # test existing save
        response = client.post(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.BAD_REQUEST.value)

        # logout
        AuthActions(client).logout()

    def test_delete_user_save(self, app: Flask, client: FlaskClient):
        """Test DELETE the user save API."""

        url = _PREFIX + "/users/saves/%s"

        user_save = None
        user = None
        with app.app_context():
            user_save = UserSave.query.first()
            user = User.query.filter_by(id=user_save.user_id).first()

        request_id = user_save.request_id

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # test valid unsave
        response = client.delete(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.NO_CONTENT.value)

        user_save = UserSave.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNone(user_save)

        # test invalid request_id
        response = client.delete(url % request_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequestEnum.NOT_FOUND.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_notifications(self, app: Flask, client: FlaskClient):
        """Test the user notifications GET API."""

        url = _PREFIX + "/users/notifications"

        notice = None
        user = None
        with app.app_context():
            notice = UserNotice.query.first()
            user = User.query.filter_by(id=notice.user_id).first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # smoke test
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # test pagination
        response = client.get(f"{url}?page=1&per_page=1")
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["pagination"]["page"], 1)
        self.assertEqual(response_data["pagination"]["per_page"], 1)

        # test filter by notice type
        notifications = UserNotice.query.filter_by(user=user).distinct(
            UserNotice.module
        )
        for notice in notifications:
            response = client.get(f"{url}?notice_type={notice.module.value}")
            self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

            response_data = response.json
            self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)
            self.assertEqual(
                response_data["data"]["user_notices"][0]["module"],
                notice.module.value,
            )

        # test filter by status
        notifications = UserNotice.query.filter_by(user=user).distinct(
            UserNotice.status
        )
        for notice in notifications:
            notice_status = "read" if notice.status is True else "unread"
            response = client.get(f"{url}?status={notice_status}")
            self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

            response_data = response.json
            self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)
            self.assertEqual(
                response_data["data"]["user_notices"][0]["status"], notice.status
            )

        # test order by update_at and update_at desc
        response = client.get(f"{url}?order_by=update_at")
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        response = client.get(f"{url}?order_by=update_at_desc")
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_notification(self, app: Flask, client: FlaskClient):
        """Test the user notification GET API."""

        url = _PREFIX + "/users/notifications/%s"

        notice = None
        user = None
        with app.app_context():
            notice = UserNotice.query.first()
            user = User.query.filter_by(id=notice.user_id).first()

        notice_id = notice.id

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url % notice_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["user_notice"]["id"], notice_id)

        # check invalid data
        response = client.get(url % 9999999999999)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

        # logout
        AuthActions(client).logout()

    def test_put_user_notification(self, app: Flask, client: FlaskClient):
        """Test the user notification PUT API."""

        url = _PREFIX + "/users/notifications/%s"

        notice = None
        user = None
        with app.app_context():
            notice = UserNotice.query.filter_by(status=False).first()
            user = User.query.filter_by(id=notice.user_id).first()

        notice_id = notice.id

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        response = client.put(url % notice_id)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.NO_CONTENT.value)

        # check db data
        with app.app_context():
            update_notice = UserNotice.query.get(notice_id)
            self.assertEqual(update_notice.status, True)

        # check invalid data
        response = client.put(url % 9999999999999)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

        # logout
        AuthActions(client).logout()

    def test_get_user_stat(self, app: Flask, client: FlaskClient):
        """Test the user stat GET API."""

        url = _PREFIX + "/users/stats"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_categories(self, app: Flask, client: FlaskClient):
        """Test the categories GET API."""

        url = _PREFIX + "/categories"

        category_num = 0
        with app.app_context():
            category_num = Category.query.count()

        # login
        AuthActions(client).login()

        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json

        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["pagination"]["page"], 1)
        self.assertEqual(response_data["pagination"]["per_page"], 10)
        self.assertEqual(response_data["pagination"]["total_items"], category_num)

        # logout
        AuthActions(client).logout()

    def test_get_category(self, app: Flask, client: FlaskClient):
        """Test the category GET API."""

        url = _PREFIX + "/categories/"

        # login
        AuthActions(client).login()

        # check valid data
        category = None
        with app.app_context():
            category = Category.query.first()

        category_id = category.id

        response = client.get(url + str(category_id))
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["category"]["id"], category_id)

        # check invalid data
        response = client.get(url + "invalid_category_id")
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

        # logout
        AuthActions(client).logout()

    def test_get_tags(self, app: Flask, client: FlaskClient):
        """Test the tags GET API."""

        url = _PREFIX + "/tags"

        tag_num = 0
        with app.app_context():
            tag_num = Tag.query.count()

        # login
        AuthActions(client).login()

        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json

        self.assertEqual(response_data["pagination"]["page"], 1)
        self.assertEqual(response_data["pagination"]["per_page"], 10)
        self.assertEqual(response_data["pagination"]["total_items"], tag_num)

        # logout
        AuthActions(client).logout()

    def test_get_tag(self, app: Flask, client: FlaskClient):
        """Test the tag GET API."""

        url = _PREFIX + "/tags/"

        # login
        AuthActions(client).login()

        # check valid data
        tag = None
        with app.app_context():
            tag = Tag.query.first()

        tag_id = tag.id

        response = client.get(url + str(tag_id))
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["tag"]["id"], tag_id)

        # check invalid data
        response = client.get(url + "invalid_tag_id")
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

        # logout
        AuthActions(client).logout()

    def test_get_stats(self, _, client: FlaskClient):
        """Test the stats GET API."""

        url = _PREFIX + "/stats"

        # login
        AuthActions(client).login()

        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()
