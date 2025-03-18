# pylint: skip-file

"""This file contains the swagger configuration."""


def get_swagger_config() -> dict:
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
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
            "schemas": schema,
        },
        "security": [{"bearerAuth": []}],
        "servers": [
            {
                "url": "http://127.0.0.1:5000/api/v1",
                "description": "Development server",
            },
            {
                "url": "https://askify-q4k0.onrender.com/api/v1",
                "description": "Production server",
            },
        ],
        "paths": path,
    }


def get_swagger_schema() -> dict:
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
                    "description": "The user password storing in hash",
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
                "update_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The user record update time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "User_Like": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The user like id",
                    "example": 1,
                },
                "user_id": {
                    "type": "string",
                    "description": "The user like user",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "request_id": {
                    "type": "integer",
                    "description": "The user like request",
                    "example": 1,
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The user like create time",
                    "example": "2024-04-21 14:36:18.896",
                },
            },
        },
        "User_Save": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The user save id",
                    "example": 1,
                },
                "user_id": {
                    "type": "string",
                    "description": "The user save user",
                    "example": "ab9ef73b-14bf-4031-a199-2ae67ce7f341",
                },
                "request_id": {
                    "type": "integer",
                    "description": "The user save request",
                    "example": 1,
                },
                "create_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The user save create time",
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
                "category_id": {
                    "type": "integer",
                    "description": "The community category id",
                    "example": 1,
                },
                "description": {
                    "type": "string",
                    "description": "The community description",
                    "example": "A community for movie lovers",
                },
                "avatar_url": {
                    "type": "string",
                    "description": "The community avatar url",
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
        "User_Notice": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The notice id",
                    "example": 1,
                },
                "user_id": {
                    "type": "string",
                    "description": "The notice user id",
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
                "module": {
                    "type": "string",
                    "description": "The notice module",
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
                "author_id": {
                    "type": "string",
                    "description": "The trending request author user id",
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
                "author_id": {
                    "type": "string",
                    "description": "The request author id",
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
                "community_id": {
                    "type": "integer",
                    "description": "The request community id",
                    "example": 1,
                },
                "category_id": {
                    "type": "integer",
                    "description": "The request category id",
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
                "request_id": {
                    "type": "integer",
                    "description": "The reply request id",
                    "example": 1,
                },
                "replier_id": {
                    "type": "string",
                    "description": "The reply replier id",
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
        "PaginationParams": {
            "type": "object",
            "properties": {
                "page": {
                    "type": "integer",
                    "description": "Page number",
                    "default": 1,
                    "minimum": 1,
                },
                "per_page": {
                    "type": "integer",
                    "description": "Items per page",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100,
                },
            },
        },
        "Stats": {
            "type": "object",
            "properties": {
                "posts_count": {"type": "integer"},
                "replies_count": {"type": "integer"},
                "likes_count": {"type": "integer"},
                "saves_count": {"type": "integer"},
            },
        },
    }


def get_swagger_path() -> dict:
    """Returns the swagger paths."""

    return {
        "/users/username/{user_name}": {
            "get": {
                "tags": ["Auth"],
                "summary": "Verify user's identity",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {
                        "name": "user_name",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User verified",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {"type": "boolean"},
                                        "message": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            }
        },
        "/users/communities": {
            "get": {
                "tags": ["User"],
                "summary": "Get user's communities",
                "security": [{"bearerAuth": []}],
                "parameters": [{"$ref": "#/components/schemas/PaginationParams"}],
                "responses": {
                    "200": {
                        "description": "Communities found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Community"
                                            },
                                        },
                                        "message": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            }
        },
        "/communities/{community_id}/join": {
            "post": {
                "tags": ["Community"],
                "summary": "Join a community",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {
                        "name": "community_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Joined community successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": None,
                                        "message": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            }
        },
        "/upload/image": {
            "post": {
                "tags": ["Upload"],
                "summary": "Upload an image",
                "security": [{"bearerAuth": []}],
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "image": {"type": "string", "format": "binary"}
                                },
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Image uploaded successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "object",
                                            "properties": {"url": {"type": "string"}},
                                        },
                                        "message": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            }
        },
        "/users/records": {
            "get": {
                "tags": ["User"],
                "summary": "Get all records by user id",
                "responses": {
                    "200": {
                        "description": "Records found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/User_Record"
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
            }
        },
        "/users/records/<record_id>": {
            "get": {
                "tags": ["User"],
                "summary": "Get a record by id",
                "parameters": [
                    {
                        "name": "record_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Record found",
                        "content": {
                            "application/json": {
                                "type": "object",
                                "properties": {
                                    "code": {"type": "integer", "example": 200},
                                    "data": {
                                        "$ref": "#/components/schemas/User_Record"
                                    },
                                    "message": {"type": "string", "example": "success"},
                                },
                            }
                        },
                    },
                },
            },
            "delete": {
                "tags": ["User"],
                "summary": "Delete a record by id",
                "parameters": [
                    {
                        "name": "record_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Record deleted successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 204},
                                        "data": None,
                                        "message": {
                                            "type": "string",
                                            "example": "delete success",
                                        },
                                    },
                                }
                            }
                        },
                    },
                },
            },
        },
        "/users/posts": {
            "get": {
                "tags": ["User"],
                "summary": "Get all posts by user id",
                "responses": {
                    "200": {
                        "description": "Posts found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Request"
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
            }
        },
        "/users/replies": {
            "get": {
                "tags": ["User"],
                "summary": "Get all replies by user id",
                "responses": {
                    "200": {
                        "description": "Replies found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Reply"
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
        "/users/likes": {
            "get": {
                "tags": ["User"],
                "summary": "Get all likes by user id",
                "responses": {
                    "200": {
                        "description": "Likes found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/User_Like"
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
            }
        },
        "/users/likes/<request_id>": {
            "post": {
                "tags": ["User"],
                "summary": "Like a request by id",
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Request liked successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 201},
                                        "data": None,
                                        "message": {
                                            "type": "string",
                                            "example": "like success",
                                        },
                                    },
                                }
                            }
                        },
                    },
                },
            },
            "delete": {
                "tags": ["User"],
                "summary": "Unlike a request by id",
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Request unliked successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 204},
                                        "data": None,
                                        "message": {
                                            "type": "string",
                                            "example": "unlike success",
                                        },
                                    },
                                }
                            }
                        },
                    }
                },
            },
        },
        "/users/saves": {
            "get": {
                "tags": ["User"],
                "summary": "Get all saves by user id",
                "responses": {
                    "200": {
                        "description": "Saves found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/User_Save"
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
            }
        },
        "/users/saves/<request_id>": {
            "post": {
                "tags": ["User"],
                "summary": "Save a request by id",
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Request saved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 201},
                                        "data": None,
                                        "message": {
                                            "type": "string",
                                            "example": "save success",
                                        },
                                    },
                                }
                            }
                        },
                    },
                },
            },
            "delete": {
                "tags": ["User"],
                "summary": "Unsave a request by id",
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Request unsaved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 204},
                                        "data": None,
                                        "message": {
                                            "type": "string",
                                            "example": "unsave success",
                                        },
                                    },
                                }
                            }
                        },
                    },
                },
            },
        },
        "/users/notifications": {
            "get": {
                "tags": ["User"],
                "summary": "Get all notifications by user id",
                "responses": {
                    "200": {
                        "description": "Notifications found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/User_Notice"
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
            }
        },
        "/users/notifications/<notice_id>": {
            "get": {
                "tags": ["User"],
                "summary": "Get a notification by id",
                "parameters": [
                    {
                        "name": "notice_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Notification found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "$ref": "#/components/schemas/User_Notice"
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "success",
                                        },
                                    },
                                }
                            },
                        },
                    },
                },
            },
            "put": {
                "tags": ["User"],
                "summary": "Update a notification by id",
                "parameters": [
                    {
                        "name": "notice_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Notification updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 204},
                                        "data": None,
                                        "message": {
                                            "type": "string",
                                            "example": "update success",
                                        },
                                    },
                                }
                            }
                        },
                    },
                },
            },
        },
        "/categories": {
            "get": {
                "tags": ["Category"],
                "summary": "Get all categories",
                "responses": {
                    "200": {
                        "description": "Categories found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "categories": {
                                                    "type": "array",
                                                    "items": {
                                                        "$ref": "#/components/schemas/Category"
                                                    },
                                                }
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
            }
        },
        "/categories/<category_id>": {
            "get": {
                "tags": ["Category"],
                "summary": "Get a category by id",
                "parameters": [
                    {
                        "name": "category_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Category found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "category": {
                                                    "$ref": "#/components/schemas/Category"
                                                }
                                            },
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "success",
                                        },
                                    },
                                }
                            },
                        },
                    },
                },
            }
        },
        "/tags": {
            "get": {
                "tags": ["Tag"],
                "summary": "Get all tags",
                "responses": {
                    "200": {
                        "description": "Tags found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Tag"
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
            }
        },
        "/tags/<tag_id>": {
            "get": {
                "tags": ["Tag"],
                "summary": "Get a tag by id",
                "parameters": [
                    {
                        "name": "tag_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Tag found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "integer", "example": 200},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "tag": {
                                                    "$ref": "#/components/schemas/Tag"
                                                }
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
                    },
                },
            }
        },
    }
