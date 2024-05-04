# pylint: skip-file

from dataclasses import dataclass

from flask import Blueprint, jsonify
from flask_sqlalchemy import pagination as Pagination

from app.constants import HttpRequstEnum

api_bp = Blueprint("api", __name__)


@dataclass
class ApiResponse:
    """Api response template data class."""

    code: HttpRequstEnum = HttpRequstEnum.SUCCESS_OK.value
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

        return jsonify(response_dict)


from . import routes
