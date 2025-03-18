# pylint: skip-file

from dataclasses import dataclass

from flask import Blueprint, jsonify
from flask_sqlalchemy.pagination import Pagination

from app.constants import HttpRequestEnum

api_bp = Blueprint("api", __name__)


@dataclass
class ApiResponse:
    """Api response template data class."""

    code: HttpRequestEnum = HttpRequestEnum.SUCCESS_OK.value
    data: object = None
    message: str = "success"
    pagination: Pagination = None

    def json(self) -> str:
        """Convert the response to JSON."""

        response_dict = {
            "code": self.code,
            "data": self.data,
            "message": self.message,
        }

        if self.pagination:
            response_dict["pagination"] = {
                "page": self.pagination.page,
                "per_page": self.pagination.per_page,
                "total_items": self.pagination.total,
                "total_pages": self.pagination.pages,
            }

        response = jsonify(response_dict)
        response.status_code = self.code
        return response


from . import routes
