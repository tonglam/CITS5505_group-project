"""Tests for the community module."""

import enum

from tests.config import TestBase


class InvalidUpdateEnum(enum.Enum):
    """Enum for invalid Create type."""

    NAME_EMPTY = "Name empty"
    CATEGORY_ID_EMPTY = "Category_id empty"
    DESCRIPTION_EMPTY = "Description empty"


class StatusEnum(enum.Enum):
    """Enum for invalid Update type."""

    SUCCESS = "ok"
    FAIL = "notok"


class TestCommunity(TestBase):
    """This class contains the test cases for the community module."""

    # def test_community(self, _, client: FlaskClient):
    #     """Test the Community page."""

    #     url = "/communities/"

    #     # test that successful communities redirects to the auth page
    #     response = client.get(url)
    #     self.assertLocationHeader(response, "/auth/auth?next=%2Fcommunities%2F")

    #     # login
    #     AuthActions(client).login()

    #     response = client.get(url)
    #     self.assertStatus(response, HttpRequestEnum.SUCCESS_OK.value)

    #     # logout
    #     AuthActions(client).logout()

    # def test_add_community(self, _, client: FlaskClient):
    #     """Test the Community page."""

    #     url = "/communities/add_community"

    #     # test that successful add_community redirects to the auth page
    #     response = client.get(url)
    #     self.assertLocationHeader(
    #         response, "/auth/auth?next=%2Fcommunities%2Fadd_community"
    #     )

    #     # login
    #     AuthActions(client).login()

    #     response = client.get(url)
    #     self.assertStatus(response, HttpRequestEnum.SUCCESS_OK.value)

    #     # logout
    #     AuthActions(client).logout()

    # def test_create_community_validate_input(self, _, client: FlaskClient):
    #     """Test the invalid create_community process."""

    #     # login
    #     AuthActions(client).login()
    #     create_community_data = [
    #         {
    #             "name": "",
    #             "description": create_seed_community_data(1)[0]["description"],
    #             "category_id": create_seed_community_data(1)[0]["category_id"],
    #             "type": InvalidUpdateEnum.NAME_EMPTY,
    #         },
    #         {
    #             "name": create_seed_community_data(1)[0]["name"],
    #             "description": "",
    #             "category_id": create_seed_community_data(1)[0]["category_id"],
    #             "type": InvalidUpdateEnum.DESCRIPTION_EMPTY,
    #         },
    #         {
    #             "name": create_seed_community_data(1)[0]["name"],
    #             "description": create_seed_community_data(1)[0]["description"],
    #             "category_id": "",
    #             "type": InvalidUpdateEnum.CATEGORY_ID_EMPTY,
    #         },
    #     ]

    #     for community_data in create_community_data:
    #         response = client.post("/communities/add_community", data=community_data)
    #         if (
    #             community_data["type"] == InvalidUpdateEnum.NAME_EMPTY
    #             or community_data["type"] == InvalidUpdateEnum.DESCRIPTION_EMPTY
    #             or community_data["type"] == InvalidUpdateEnum.CATEGORY_ID_EMPTY
    #         ):
    #             self.assertEqual(json.loads(response.data)["ok"], StatusEnum.FAIL.value)
    #         else:
    #             self.assertEqual(
    #                 json.loads(response.data)["ok"], StatusEnum.SUCCESS.value
    #             )

    # def test_edit_community(self, _, client: FlaskClient):
    #     """Test the edit page."""

    #     url = "/communities/editCommunity/1"

    #     # test that successful editCommunity redirects to the auth page
    #     response = client.get(url)
    #     self.assertLocationHeader(
    #         response, "/auth/auth?next=%2Fcommunities%2FeditCommunity%2F1"
    #     )

    #     # login
    #     AuthActions(client).login()

    #     response = client.get(url)
    #     self.assertStatus(response, HttpRequestEnum.SUCCESS_OK.value)

    #     # logout
    #     AuthActions(client).logout()

    # def test_create_edit_delete_community(self, _, client: FlaskClient):
    #     """Test the create_edit_delete process."""
    #     # login
    #     AuthActions(client).login()

    #     # Test creating a new community.
    #     community_data = {
    #         "name": create_seed_community_data(1)[0]["name"],
    #         "description": create_seed_community_data(1)[0]["description"],
    #         "category_id": create_seed_community_data(1)[0]["category_id"],
    #     }
    #     response = client.post("/communities/add_community", data=community_data)
    #     self.assertStatus(response, HttpRequestEnum.SUCCESS_OK.value)
    #     self.assertIn("id", response.json)
    #     community_id = response.json["id"]
    #     # Verify that the community has been created in the database
    #     created_community = Community.query.get(community_id)
    #     self.assertIsNotNone(created_community)
    #     self.assertEqual(created_community.name, community_data["name"])
    #     self.assertEqual(created_community.description, community_data["description"])
    #     self.assertEqual(
    #         created_community.category_id, int(community_data["category_id"])
    #     )

    #     # Test edit a community.
    #     community_data = {
    #         "name": create_seed_community_data(1)[0]["name"],
    #         "description": create_seed_community_data(1)[0]["description"],
    #         "category_id": create_seed_community_data(1)[0]["category_id"],
    #     }
    #     response = client.post(
    #         f"/communities/update_community/{community_id}", data=community_data
    #     )
    #     self.assertEqual(json.loads(response.data)["ok"], StatusEnum.SUCCESS.value)
    #     # Verify that the community has been modified in the database
    #     created_community = Community.query.get(community_id)
    #     self.assertIsNotNone(created_community)
    #     self.assertEqual(created_community.name, community_data["name"])
    #     self.assertEqual(created_community.description, community_data["description"])
    #     self.assertEqual(
    #         created_community.category_id, int(community_data["category_id"])
    #     )

    #     # Test delete a community.
    #     response = client.delete(f"/communities/update_community/{community_id}")
    #     self.assertEqual(json.loads(response.data)["ok"], StatusEnum.SUCCESS.value)

    #     # Verified community has been deleted
    #     deleted_community = Community.query.get(community_id)
    #     self.assertIsNone(deleted_community)
    #     # logout
    #     AuthActions(client).logout()

    # def test_update_community_validate_input(self, _, client: FlaskClient):
    #     """Test the invalid create_community process."""

    #     # login
    #     AuthActions(client).login()
    #     community_data = {
    #         "name": create_seed_community_data(1)[0]["name"],
    #         "description": create_seed_community_data(1)[0]["description"],
    #         "category_id": create_seed_community_data(1)[0]["category_id"],
    #     }
    #     response = client.post("/communities/add_community", data=community_data)
    #     self.assertStatus(response, HttpRequestEnum.SUCCESS_OK.value)
    #     self.assertStatus(response, HttpRequestEnum.SUCCESS_OK.value)
    #     self.assertIn("id", response.json)
    #     community_id = response.json["id"]
    #     create_community_data = [
    #         {
    #             "name": "",
    #             "description": create_seed_community_data(1)[0]["description"],
    #             "category_id": create_seed_community_data(1)[0]["category_id"],
    #             "type": InvalidUpdateEnum.NAME_EMPTY,
    #         },
    #         {
    #             "name": create_seed_community_data(1)[0]["name"],
    #             "description": "",
    #             "category_id": create_seed_community_data(1)[0]["category_id"],
    #             "type": InvalidUpdateEnum.DESCRIPTION_EMPTY,
    #         },
    #         {
    #             "name": create_seed_community_data(1)[0]["name"],
    #             "description": create_seed_community_data(1)[0]["description"],
    #             "category_id": "",
    #             "type": InvalidUpdateEnum.CATEGORY_ID_EMPTY,
    #         },
    #     ]

    #     for community_data in create_community_data:
    #         response = client.post(
    #             f"/communities/update_community/{community_id}", data=community_data
    #         )
    #         if (
    #             community_data["type"] == InvalidUpdateEnum.NAME_EMPTY
    #             or community_data["type"] == InvalidUpdateEnum.DESCRIPTION_EMPTY
    #             or community_data["type"] == InvalidUpdateEnum.CATEGORY_ID_EMPTY
    #         ):
    #             self.assertEqual(json.loads(response.data)["ok"], StatusEnum.FAIL.value)
    #         else:
    #             self.assertEqual(
    #                 json.loads(response.data)["ok"], StatusEnum.SUCCESS.value
    #             )
