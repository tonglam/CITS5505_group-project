"""Tests for the API module."""

from datetime import datetime

from flask import Flask
from flask.testing import FlaskClient

from app.constants import HttpRequstEnum
from app.models.category import Category
from app.models.reply import Reply
from app.models.request import Request
from app.models.tag import Tag
from app.models.user import User
from app.models.user_like import UserLike
from app.models.user_notice import UserNotice
from app.models.user_record import UserRecord
from app.models.user_save import UserSave
from tests.config import AuthActions, TestBase

_PREFIX = "/api/v1"


class TestApi(TestBase):
    """This class contains the test cases for the API module."""

    # def test_get_users(self, app: Flask, client: FlaskClient):
    #     """Test the users GET API."""

    #     url = _PREFIX + "/users/"

    #     # check valid data
    #     user = None
    #     with app.app_context():
    #         user = User.query.first()

    #     username = user.username

    #     # login
    #     AuthActions(client).login(email=user.email, password="Password@123")

    #     response = client.get(url + username)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

    #     response_data = response.json
    #     self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response_data["data"]["user"]["username"], username)

    #     # check invalid data
    #     response = client.get(url + "invalid_user_id")
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

    #     response_data = response.json
    #     self.assertEqual(response_data["code"], HttpRequstEnum.NOT_FOUND.value)
    #     self.assertEqual(response_data["data"], None)

    #     # logout
    #     AuthActions(client).logout()

    # def test_put_users(self, app: Flask, client: FlaskClient):
    #     """Test the users PUT API."""

    #     url = _PREFIX + "/users/"

    #     user = None
    #     with app.app_context():
    #         user = User.query.first()

    #     username = user.username

    #     # login
    #     AuthActions(client).login(email=user.email, password="Password@123")

    #     update_data = {
    #         "username": "test_" + user.username,
    #         "email": "test_" + user.email,
    #         "avatar_url": "https://api.dicebear.com/5.x/adventurer/svg?seed=test",
    #         "use_google": True,
    #         "use_github": True,
    #         "security_question": "test_" + user.security_question,
    #         "security_answer": "test_" + user.security_answer,
    #         "status": UserStatusEnum.INACTIVE.value,
    #     }

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

    #     response_data = response.json
    #     self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

    #     # check the updated data
    #     update_username = response_data["data"]["user"]["username"]
    #     update_email = response_data["data"]["user"]["email"]
    #     update_avatar_url = response_data["data"]["user"]["avatar_url"]
    #     update_use_google = response_data["data"]["user"]["use_google"]
    #     update_use_github = response_data["data"]["user"]["use_github"]
    #     update_security_question = response_data["data"]["user"]["security_question"]
    #     update_security_answer = response_data["data"]["user"]["security_answer"]
    #     update_status = response_data["data"]["user"]["status"]

    #     self.assertEqual(update_username, "test_" + user.username)
    #     self.assertEqual(update_email, "test_" + user.email)
    #     self.assertEqual(
    #         update_avatar_url, "https://api.dicebear.com/5.x/adventurer/svg?seed=test"
    #     )
    #     self.assertEqual(update_use_google, True)
    #     self.assertEqual(update_use_github, True)
    #     self.assertEqual(update_security_question, "test_" + user.security_question)
    #     self.assertEqual(update_security_answer, "test_" + user.security_answer)
    #     self.assertEqual(update_status, UserStatusEnum.INACTIVE.value)

    #     # check db data
    #     with app.app_context():
    #         update_user = User.query.filter_by(username=update_username).first()
    #         self.assertEqual(update_user.username, update_username)
    #         self.assertEqual(update_user.email, update_email)
    #         self.assertEqual(update_user.avatar_url, update_avatar_url)
    #         self.assertEqual(update_user.use_google, update_use_google)
    #         self.assertEqual(update_user.use_github, update_use_github)
    #         self.assertEqual(update_user.security_question, update_security_question)
    #         self.assertEqual(update_user.security_answer, update_security_answer)
    #         self.assertEqual(update_user.status, update_status)

    #     # check notice
    #     notice = UserNotice.query.filter_by(
    #         user=user, module=UserNoticeModuleEnum.USER, status=False
    #     ).first()
    #     self.assertIsNotNone(notice)

    #     # logout
    #     AuthActions(client).logout()

    # def test_invalid_put_users(self, app: Flask, client: FlaskClient):
    #     """Test the invalid users PUT API."""

    #     url = _PREFIX + "/users/"

    #     user = None
    #     with app.app_context():
    #         user = User.query.first()

    #     username = user.username

    #     # check permission
    #     AuthActions(client).login()

    #     response = client.put(
    #         url + username,
    #         json={"username": "test_" + user.username},
    #     )
    #     self.assertEqual(response.status_code, HttpRequstEnum.FORBIDDEN.value)

    #     AuthActions(client).logout()

    #     # login
    #     AuthActions(client).login(email=user.email, password="Password@123")

    #     # check empty data
    #     response = client.put(url + username, json={})
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "request data is empty")

    #     # check if the username is a string
    #     update_data = {"username": 123}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[username] must be a string")

    #     # check if the username already exists
    #     another_user = None
    #     with app.app_context():
    #         another_user = User.query.filter(User.id != user.id).first()

    #     update_data = {"username": another_user.username}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[username] already exists")

    #     # check if the email is a string
    #     update_data = {"email": 123}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[email] must be a string")

    #     # check if the email is not a valid email
    #     update_data = {"email": user.email + ".invalid"}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[email] is invalid")

    #     # check if the avatar_url is a string
    #     update_data = {"avatar_url": 123}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[avatar_url] must be a string")

    #     # check if the use_google is a boolean
    #     update_data = {"use_google": 123}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[use_google] must be a boolean")

    #     # check if the use_github is a boolean
    #     update_data = {"use_github": 123}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[use_github] must be a boolean")

    #     # check if the security_question is a string
    #     update_data = {"security_question": 123}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(
    #         response.json["message"], "[security_question] must be a string"
    #     )

    #     # check if the security_answer is a string
    #     update_data = {"security_answer": 123}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[security_answer] must be a string")

    #     # check if the status is a string
    #     update_data = {"status": 123}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)

    #     # check if the status is invalid
    #     update_data = {"status": "invalid_status"}

    #     response = client.put(url + username, json=update_data)
    #     self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
    #     self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
    #     self.assertEqual(response.json["message"], "[status] is invalid")

    #     # logout
    #     AuthActions(client).logout()

    def test_get_user_records(self, app: Flask, client: FlaskClient):
        """Test the user records GET API."""

        url = _PREFIX + "/users/records"

        user_record = None
        with app.app_context():
            user_record = UserRecord.query.first()
            user = User.query.get(user_record.user_id)

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # Test case 1: No filter or sorting parameters provided
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        # Test case 2: Only filter parameters provided
        response = client.get(f"{url}?request_id=1&record_type=REQUEST")
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        # Test case 3: Only sorting parameter provided
        response = client.get(f"{url}?order_by=update_at")
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        # Test case 4: Both filter and sorting parameters provided
        response = client.get(
            f"{url}?request_id=1&record_type=REQUEST&order_by=update_at"
        )
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_user_record(self, app: Flask, client: FlaskClient):
        """Test the user records API."""

        url = _PREFIX + "/users/records/%s"

        user = None
        user_record = None
        with app.app_context():
            user_record = UserRecord.query.first()
            user = User.query.get(user_record.user_id)

        record_id = user_record.id

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url % record_id)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["user_record"]["id"], record_id)

        response = client.delete(url % record_id)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequstEnum.NO_CONTENT.value)

        # check db
        with app.app_context():
            record = UserRecord.query.get(record_id)
            self.assertEqual(record, None)

        # check invalid data
        response = client.delete(url % 9999999999999)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequstEnum.NOT_FOUND.value)

        # logout
        AuthActions(client).logout()

    def test_user_posts(self, app: Flask, client: FlaskClient):
        """Test the user posts API."""

        url = _PREFIX + "/users/posts"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        user_posts_count = Request.query.filter_by(author_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_posts"]), min(user_posts_count, 10)
        )

        # logout
        AuthActions(client).logout()

    def test_user_replies(self, app: Flask, client: FlaskClient):
        """Test the user replies API."""

        url = _PREFIX + "/users/replies"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        user_replies_count = Reply.query.filter_by(replier_id=user.id).count()
        self.assertEqual(
            len(response_data["data"]["user_replies"]), min(user_replies_count, 10)
        )

        # logout
        AuthActions(client).logout()

    def test_user_likes(self, app: Flask, client: FlaskClient):
        """Test the user likes API."""

        url = _PREFIX + "/users/likes"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.CREATED.value)

        user_like = UserLike.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNotNone(user_like)

        # test invalid request_id
        response = client.post(url % 9999999)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequstEnum.NOT_FOUND.value)

        # test existing like
        response = client.post(url % request_id)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)

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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NO_CONTENT.value)

        user_like = UserLike.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNone(user_like)

        # test invalid request_id
        response = client.delete(url % request_id)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequstEnum.NOT_FOUND.value)

        # logout
        AuthActions(client).logout()

    def test_user_saves(self, app: Flask, client: FlaskClient):
        """Test the user saves API."""

        url = _PREFIX + "/users/saves"

        user = None
        with app.app_context():
            user = User.query.first()

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # check valid data
        response = client.get(url)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.CREATED.value)

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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.CREATED.value)
        self.assertEqual(response_data["message"], "save success")

        user_save = UserSave.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNotNone(user_save)

        # test invalid request_id
        response = client.post(url % 9999999)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequstEnum.NOT_FOUND.value)

        # test existing save
        response = client.post(url % request_id)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)

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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NO_CONTENT.value)
        self.assertEqual(response_data["message"], "unsave success")

        user_save = UserSave.query.filter_by(
            user_id=user.id, request_id=request_id
        ).first()
        self.assertIsNone(user_save)

        # test invalid request_id
        response = client.delete(url % request_id)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response.json["code"], HttpRequstEnum.NOT_FOUND.value)

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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        # test pagination
        response = client.get(f"{url}?page=1&per_page=1")
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["pagination"]["page"], 1)
        self.assertEqual(response_data["pagination"]["per_page"], 1)

        # test filter by notice type
        notifications = UserNotice.query.filter_by(user=user).distinct(
            UserNotice.module
        )
        for notice in notifications:
            response = client.get(f"{url}?notice_type={notice.module.value}")
            self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

            response_data = response.json
            self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
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
            self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

            response_data = response.json
            self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
            self.assertEqual(
                response_data["data"]["user_notices"][0]["status"], notice.status
            )

        # test order by update_at and update_at desc
        response = client.get(f"{url}?order_by=update_at")
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertGreaterEqual(
            datetime.strptime(
                response_data["data"]["user_notices"][1]["update_at"],
                "%a, %d %b %Y %H:%M:%S %Z",
            ),
            datetime.strptime(
                response_data["data"]["user_notices"][0]["update_at"],
                "%a, %d %b %Y %H:%M:%S %Z",
            ),
        )

        response = client.get(f"{url}?order_by=update_at_desc")
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertGreaterEqual(
            datetime.strptime(
                response_data["data"]["user_notices"][0]["update_at"],
                "%a, %d %b %Y %H:%M:%S %Z",
            ),
            datetime.strptime(
                response_data["data"]["user_notices"][1]["update_at"],
                "%a, %d %b %Y %H:%M:%S %Z",
            ),
        )

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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["user_notice"]["id"], notice_id)

        # check invalid data
        response = client.get(url % 9999999999999)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NOT_FOUND.value)
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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NO_CONTENT.value)

        # check db data
        with app.app_context():
            update_notice = UserNotice.query.get(notice_id)
            self.assertEqual(update_notice.status, True)

        # check invalid data
        response = client.put(url % 9999999999999)
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json

        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["category"]["id"], category_id)

        # check invalid data
        response = client.get(url + "invalid_category_id")
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NOT_FOUND.value)
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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

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
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["tag"]["id"], tag_id)

        # check invalid data
        response = client.get(url + "invalid_tag_id")
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

        # logout
        AuthActions(client).logout()

    def test_search(self, _, client: FlaskClient):
        """Test the search API."""

        url = _PREFIX + "/search"

        # login
        AuthActions(client).login()

        # check valid data
        response = client.get(url + "?keyword=is")
        self.assertEqual(response.status_code, HttpRequstEnum.SUCCESS_OK.value)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()
