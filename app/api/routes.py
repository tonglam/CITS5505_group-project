"""Routes for api."""

from dataclasses import asdict, dataclass

from flask import jsonify

from app.api import api_bp
from app.constant import HttpRequstEnum
from app.models.user import User
from app.models.user_record import UserRecord


@dataclass
class ApiResponse:
    """Api response template dat class."""

    code: HttpRequstEnum = HttpRequstEnum.SUCCESS_OK.value
    data: object = None
    message: str = "success"

    def json(self) -> str:
        """Convert the response to JSON."""
        return jsonify(asdict(self))


# Api for auth module.


# Api for user module.


@api_bp.route("/users/<user_id>", methods=["GET"])
def users(user_id: str):
    """Get a user by id."""
    user = User.query.get(user_id)
    if user is None:
        return ApiResponse(
            HttpRequstEnum.BAD_REQUEST.value, data={"user_id": ""}
        ).json()
    return ApiResponse(data={"user_id": user_id}).json()


@api_bp.route("/users/records/<user_id>", methods=["GET"])
def records(user_id: str):
    """Get records of a user by id."""
    user_records = UserRecord.query.filter_by(user_id=user_id).first()
    records_data = user_records.records if user_records else []
    print("records", records_data)
    return ApiResponse(data={"records": records_data}).json()


# Api for community module.


# Api for popular module.


# Api for post module.


# Api for search module.


# Api for notice module.
