"""This file contains the swagger configuration."""


def get_swagger_config():
    """Returns the swagger configuration."""

    path = get_swagger_path()
    schema = get_swagger_schema()

    return {
        "swagger": "3.0",
        "uiversion": 3,
        "openapi": "3.0.0",
        "title": "Request Forum API",
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "info": {
            "title": "Request Forum API",
            "version": "1.0.0",
            "description": "This is the API documentation for the Request Forum.",
        },
        "basePath": "/api/v1",
        "components": {
            "securitySchemes": {
                "cookieAuth": {
                    "type": "apiKey",
                    "in": "cookie",
                    "name": "access_token",
                },
            },
            "schemas": schema,
        },
        "servers": [
            {"url": "http://127.0.0.1:5000/api/v1", "description": "Development server"}
        ],
        "paths": path,
    }


def get_swagger_schema():
    """Returns the swagger definitions."""

    return {
        "User": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "The user id",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "username": {
                    "type": "string",
                    "description": "The username",
                    "example": "test",
                },
                "email": {
                    "type": "string",
                    "description": "The user email",
                    "example": "test@example.com",
                },
                "password_hash": {
                    "type": "string",
                    "description": "The user password storing in shash",
                    "example": "$2b$12$R49DZkkWelMYoCv2.mCQeemIVKkCNrzuA3Vekq6PxMpIk4jqjJbmW",
                },
                "avatar_url": {
                    "type": "string",
                    "description": "The user avatar url",
                    "example": "https://example.com/avatar.png",
                },
                "use_google": {
                    "type": "boolean",
                    "description": "If the user use google login",
                    "example": True,
                },
                "use_github": {
                    "type": "boolean",
                    "description": "If the user use github login",
                    "example": True,
                },
                "security_question": {
                    "type": "string",
                    "description": "The user security question",
                    "example": "What is your favorite color?",
                },
                "security_answer": {
                    "type": "string",
                    "description": "The user security answer",
                    "example": "blue",
                },
                "status": {
                    "type": "string",
                    "description": "The user status",
                    "enum": ["active", "inactive"],
                    "example": "active",
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The user create time",
                    "example": "2024-04-21 14:36:18.896",
                },
                "update_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The user update time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "Category": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The category id",
                    "example": 1,
                },
                "name": {
                    "type": "string",
                    "description": "The category name",
                    "example": "movie",
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The category create time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "Tag": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The tag id",
                    "example": 1,
                },
                "name": {
                    "type": "string",
                    "description": "The tag name",
                    "example": "LossRecovery",
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The tag create time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "Community": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The community id",
                    "example": 1,
                },
                "name": {
                    "type": "string",
                    "description": "The community name",
                    "example": "Cinema Club",
                },
                "category": {
                    "type": "integer",
                    "description": "The community category",
                    "example": 1,
                },
                "description": {
                    "type": "string",
                    "description": "The community description",
                    "example": "A community for movie lovers",
                },
                "avatar": {
                    "type": "string",
                    "description": "The community avatar",
                    "example": "https://example.com/avatar.png",
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The community create time",
                    "example": "2024-04-21 14:36:18.896",
                },
                "update_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The community update time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "Notice": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The notice id",
                    "example": 1,
                },
                "user": {
                    "type": "string",
                    "description": "The notice user",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "subject": {
                    "type": "string",
                    "description": "The notice subject",
                    "example": "Notification: System",
                },
                "content": {
                    "type": "string",
                    "description": "The notice content",
                    "example": "Announcement successfully!",
                },
                "notice_type": {
                    "type": "string",
                    "description": "The notice type",
                    "enum": [
                        "System",
                        "User",
                        "Post",
                        "Comment",
                        "Reply",
                        "Like",
                        "Follow",
                        "Save",
                        "Community",
                    ],
                    "example": "System",
                },
                "status": {
                    "type": "boolean",
                    "description": "The notice status",
                    "enum": [True, False],
                    "example": False,
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The notice create time",
                    "example": "2024-04-21 14:36:18.896",
                },
                "update_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The notice update time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "Trending": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The trending id",
                    "example": 1,
                },
                "request_id": {
                    "type": "integer",
                    "description": "The trending request id",
                    "example": 1,
                },
                "title": {
                    "type": "string",
                    "description": "The trending request title",
                    "example": "Movie Night Suggestions",
                },
                "author": {
                    "type": "string",
                    "description": "The trending request author",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "reply_num": {
                    "type": "integer",
                    "description": "The trending request reply number",
                    "example": 1,
                },
                "date": {
                    "type": "string",
                    "description": "The trending date",
                    "example": "2024-04-21",
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The trending create time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "Request": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The request id",
                    "example": 1,
                },
                "community": {
                    "type": "integer",
                    "description": "The request community",
                    "example": 1,
                },
                "author": {
                    "type": "string",
                    "description": "The request author",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "title": {
                    "type": "string",
                    "description": "The request title",
                    "example": "What a great movie!",
                },
                "content": {
                    "type": "string",
                    "description": "The request content",
                    "example": "I watched a great movie last night.",
                },
                "category": {
                    "type": "integer",
                    "description": "The request category",
                    "example": 1,
                },
                "view_num": {
                    "type": "integer",
                    "description": "The request view number",
                    "example": 1,
                },
                "like_num": {
                    "type": "integer",
                    "description": "The request like number",
                    "example": 1,
                },
                "reply_num": {
                    "type": "integer",
                    "description": "The request reply number",
                    "example": 1,
                },
                "save_num": {
                    "type": "integer",
                    "description": "The request save number",
                    "example": 1,
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The request create time",
                    "example": "2024-04-21 14:36:18.896",
                },
                "update_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The request update time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "Reply": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The reply id",
                    "example": 1,
                },
                "request": {
                    "type": "integer",
                    "description": "The reply request",
                    "example": 1,
                },
                "replier": {
                    "type": "string",
                    "description": "The reply replier",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "content": {
                    "type": "string",
                    "description": "The reply content",
                    "example": "I agree with you.",
                },
                "source": {
                    "type": "integer",
                    "description": "The reply source",
                    "enum": ["HUMAN", "AI"],
                    "example": "HUMAN",
                },
                "like_num": {
                    "type": "integer",
                    "description": "The reply like number",
                    "example": 1,
                },
                "save_num": {
                    "type": "integer",
                    "description": "The reply save number",
                    "example": 1,
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The reply create time",
                    "example": "2024-04-21 14:36:18.896",
                },
                "update_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The reply update time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "User_Preference": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The user preference id",
                    "example": 1,
                },
                "user_id": {
                    "type": "string",
                    "description": "The user preference user",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "communities": {
                    "type": "array",
                    "description": "The user preference communities",
                    "items": {"type": "integer"},
                    "example": [1, 2],
                },
                "interests": {
                    "type": "array",
                    "description": "The user preference interests",
                    "items": {"type": "integer"},
                    "example": [1, 2],
                },
                "update_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The user preference update time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "User_Record": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The user record id",
                    "example": 1,
                },
                "user_id": {
                    "type": "string",
                    "description": "The user record user",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "request_id": {
                    "type": "integer",
                    "description": "The user record request",
                    "example": 1,
                },
                "record_type": {
                    "type": "string",
                    "description": "The user record type",
                    "enum": ["REQUEST", "REPLY", "VIEW", "LIKE", "SAVE"],
                    "example": "LIKE",
                },
                "update_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The user record update time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
    }


def get_swagger_path():
    """Returns the swagger paths."""

    return {
        "/users/{user_id}": {
            "get": {
                "tags": ["User"],
                "summary": "Get a user by id",
                "security": [{"cookieAuth": []}],
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "description": "The user id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Get a user by id successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {
                                            "type": "integer",
                                            "example": 200,
                                        },
                                        "data": {
                                            "$ref": "#/components/schemas/User",
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "success",
                                        },
                                    },
                                }
                            }
                        },
                    }
                },
            },
            "put": {
                "tags": ["User"],
                "summary": "Update a user by id",
                "security": [{"cookieAuth": []}],
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "description": "The user id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/User",
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Update a user by id successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {
                                            "type": "integer",
                                            "example": 200,
                                        },
                                        "data": {
                                            "$ref": "#/components/schemas/User",
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "success",
                                        },
                                    },
                                }
                            }
                        },
                    }
                },
            },
        },
        "/users/{user_id}/records": {
            "get": {
                "tags": ["User"],
                "summary": "Get a user record by id",
                "security": [{"cookieAuth": []}],
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "description": "The user id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Get a user record by id successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {
                                            "type": "integer",
                                            "example": 200,
                                        },
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/User_Record",
                                            },
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "success",
                                        },
                                    },
                                }
                            }
                        },
                    }
                },
            },
        },
        "/users/{user_id}/preferences": {
            "get": {
                "tags": ["User"],
                "summary": "Get a user preference by id",
                "security": [{"cookieAuth": []}],
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "description": "The user id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Get a user preference by id successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {
                                            "type": "integer",
                                            "example": 200,
                                        },
                                        "data": {
                                            "$ref": "#/components/schemas/User_Preference",
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "success",
                                        },
                                    },
                                }
                            }
                        },
                    }
                },
            },
            "/users/{user_id}/pre
            "/categories": {
                "get": {
                    "tags": ["Category"],
                    "summary": "Get all categories",
                    "security": [{"cookieAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Get all categories successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "code": {
                                                "type": "integer",
                                                "example": 200,
                                            },
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/Category",
                                                },
                                            },
                                            "message": {
                                                "type": "string",
                                                "example": "success",
                                            },
                                        },
                                    }
                                }
                            },
                        }
                    },
                },
            },
            "/categories/{category_id}": {
                "get": {
                    "tags": ["Category"],
                    "summary": "Get a category by id",
                    "security": [{"cookieAuth": []}],
                    "parameters": [
                        {
                            "name": "category_id",
                            "in": "path",
                            "description": "The category id",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Get a category by id successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "code": {
                                                "type": "integer",
                                                "example": 200,
                                            },
                                            "data": {
                                                "$ref": "#/components/schemas/Category",
                                            },
                                            "message": {
                                                "type": "string",
                                                "example": "success",
                                            },
                                        },
                                    }
                                }
                            },
                        }
                    },
                },
            },
            "/tags": {
                "get": {
                    "tags": ["Tag"],
                    "summary": "Get all tags",
                    "security": [{"cookieAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Get all tags successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "code": {
                                                "type": "integer",
                                                "example": 200,
                                            },
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/Tag",
                                                },
                                            },
                                            "message": {
                                                "type": "string",
                                                "example": "success",
                                            },
                                        },
                                    }
                                }
                            },
                        }
                    },
                },
            },
            "/tags/{tag_id}": {
                "get": {
                    "tags": ["Tag"],
                    "summary": "Get a tag by id",
                    "security": [{"cookieAuth": []}],
                    "parameters": [
                        {
                            "name": "tag_id",
                            "in": "path",
                            "description": "The tag id",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Get a tag by id successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "code": {
                                                "type": "integer",
                                                "example": 200,
                                            },
                                            "data": {
                                                "$ref": "#/components/schemas/Tag",
                                            },
                                            "message": {
                                                "type": "string",
                                                "example": "success",
                                            },
                                        },
                                    }
                                }
                            },
                        }
                    },
                },
            },
        },
    }
