REGISTER_DOCS = """
    register - API for register new user with user role.

    ## Role Choice
        ADMIN = "admin", _("Admin")
        AUTHOR = "author", _("Author")
        VIEWER = "viewer", _("Viewer")
    
    # Sample Request Data
        {
            "username": "adminuser",
            "email": "adminuser@yopmail.com",
            "password": "Admin@123",
            "role": "admin",
            "first_name": "admin",
            "last_name": "user"
        }

    # Success Response Data
        {
            "success": true,
            "message": "User created successfully.",
            "payload": {
                "id": 1,
                "last_login": null,
                "is_superuser": false,
                "username": "adminuser",
                "first_name": "admin",
                "last_name": "user",
                "is_staff": false,
                "is_active": true,
                "is_delete": false,
                "date_joined": "2024-12-22T15:21:20.581871",
                "role": "admin",
                "email": "adminuser@yopmail.com"
            }
        }
    """


LOGIN_DOCS = """
    login - API for login user.

    # Sample Request Data
        {
            "email": "adminuser@yopmail.com",
            "password": "Secure@098"
        }

    # Success Response Data
        {
            "success": true,
            "message": "Login successful.",
            "payload": {
                "user": {
                    "id": 2,
                    "last_login": null,
                    "is_superuser": false,
                    "username": "adminuser",
                    "first_name": "admin",
                    "last_name": "user",
                    "is_staff": false,
                    "is_active": true,
                    "date_joined": "2024-12-22T18:30:20.327271",
                    "role": "admin",
                    "email": "adminuser@yopmail.com",
                    "is_delete": false
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0OTcyNDA2LCJpYXQiOjE3MzQ4ODYwMDYsImp0aSI6ImUzNWVkNWU3NzFlYTQxNmY5NTVlYTIyOGZmOTRjOTdjIiwidXNlcl9pZCI6Mn0.gTENnot7eXT4j-4o2XHqxABYDCrHbYOU0twovVNLCP8",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDk3MjQwNiwiaWF0IjoxNzM0ODg2MDA2LCJqdGkiOiI4YTYxZTI5MTVjMDk0YjFkOGY1OWM0ODZjMDIzOGMwNSIsInVzZXJfaWQiOjJ9.O1xDSCh7_Tcf4uqoKmnmEaTl3WROeR2qm8uOT4C6Nsg"
            }
        }
    """


USER_DOCS = """
    # RetrieveUsers : API for get user list with filter and pagination.
    - `http://localhost:8000/api/users/?page=1&page_size=1&role=viewer`

    ## Success Response Data
        {
            "success": true,
            "message": "Users list fetched successfully.",
            "payload": {
                "count": 5,
                "next": "http://localhost:8000/api/users/?page=2&page_size=2",
                "previous": null,
                "results": [
                    {
                        "id": 6,
                        "last_login": null,
                        "is_superuser": false,
                        "username": "vieweruser",
                        "first_name": "viewer",
                        "last_name": "user",
                        "is_staff": false,
                        "is_active": true,
                        "date_joined": "2024-12-22T22:03:03.716529",
                        "role": "viewer",
                        "email": "viewerser@yopmail.com",
                        "is_delete": false
                    }
                ]
            }
        }

    # GetUser : API for get user by id.
    - `http://localhost:8000/api/users/4/`

    ## Success Response Data
        {
            "success": true,
            "message": "User retrieved successfully.",
            "payload": {
                "id": 4,
                "last_login": null,
                "is_superuser": false,
                "username": "vieweruser1",
                "first_name": "viewer",
                "last_name": "user1",
                "is_staff": false,
                "is_active": true,
                "date_joined": "2024-12-22T18:37:30",
                "role": "viewer",
                "email": "vieweruser@yopmail.com",
                "is_delete": false
            }
        }
        
    # UpdateUser : API for update user by id.
    - `http://localhost:8000/api/users/4/`

    ## Success Response Data
        {
            "success": true,
            "message": "User details updated successfully.",
            "payload": {
                "id": 4,
                "last_login": null,
                "is_superuser": false,
                "username": "vieweruser1",
                "first_name": "viewer",
                "last_name": "user1",
                "is_staff": false,
                "is_active": true,
                "date_joined": "2024-12-22T18:37:30",
                "role": "viewer",
                "email": "vieweruser@yopmail.com",
                "is_delete": false
            }
        }
        
    # DeleteUser : API for delete user by id.
    - `http://localhost:8000/api/users/5/`

    ## Success Response Data
        {
            "success": true,
            "message": "User deleted successfully."
        }
    """


ARTICLE_DOCS = """
    # CreateArticle : API for create articles based on user permission.
    - `http://localhost:8000/api/article/`
    
    ## Sample Request Data
        {
            "title": "article1",
            "body": "testing article"
        }

    ## Success Response Data
        {
            "success": true,
            "message": "Article created successfully.",
            "payload": {
                "id": 6,
                "title": "article1",
                "body": "testing article",
                "author": 2,
                "published": false,
                "created_at": "2024-12-23T00:04:04.796664",
                "updated_at": "2024-12-23T00:04:04.796691"
            }
        }

    # RetrieveArticles : API for get list of articles based on pagination and filter
    - `http://localhost:8000/api/articles/?author__email=adminuser@yopmail.com&page=1&page_size=1`

    ## Success Response Data
        {
            "success": true,
            "message": "Articles retrieved successfully.",
            "payload": {
                "count": 4,
                "next": "http://localhost:8000/api/articles/?author__email=adminuser%40yopmail.com&page=2&page_size=1",
                "previous": null,
                "results": [
                    {
                        "id": 6,
                        "title": "str2",
                        "body": "string",
                        "author": 2,
                        "published": false,
                        "created_at": "2024-12-23T00:04:04.796664",
                        "updated_at": "2024-12-23T00:04:04.796691"
                    }
                ]
            }
        }
        
    # GetArticle : API for get article by id.
    - `http://localhost:8000/api/articles/5/`

    ## Success Response Data
        {
            "success": true,
            "message": "Article retrieved successfully.",
            "payload": {
                "id": 5,
                "title": "string",
                "body": "string",
                "author": 2,
                "published": false,
                "created_at": "2024-12-23T00:03:10.820392",
                "updated_at": "2024-12-23T00:03:10.820412"
            }
        }
    
    # PublishArticle : API for publish/unpublish article.
    - `http://localhost:8000/api/article/2/publish/`
    
    ## Sample Request Data
        {
            "is_published": true
        }

    ## Success Response Data
        {
            "success": true,
            "message": "Article published successfully.",
            "payload": {
                "id": 5,
                "title": "string",
                "body": "string",
                "author": 2,
                "published": true,
                "created_at": "2024-12-23T00:03:10.820392",
                "updated_at": "2024-12-23T00:03:10.820412"
            }
        }
        
    # UpdateArticle : API for update article.
    - `http://localhost:8000/api/article/4/`
    
    ## Sample Request Data
        {
            "title": "string",
            "body": "string"
        }

    ## Success Response Data
        {
            "success": true,
            "message": "Article updated successfully.",
            "payload": {
                "id": 5,
                "title": "string",
                "body": "string",
                "author": 2,
                "published": true,
                "created_at": "2024-12-23T00:03:10.820392",
                "updated_at": "2024-12-23T00:03:10.820412"
            }
        }
        
    # DeleteArticle : API for delete article.
    - `http://localhost:8000/api/articles/6/`

    ## Success Response Data
        {
            "success": true,
            "message": "Article deleted successfully."
        }
    """


COMMENT_DOCS = """
    # AddComment : API for add comment.
    - `http://localhost:8000/api/articles/2/comments/`
    
    ## Sample Request Data
        {
            "body": "comment1"
        }

    ## Success Response Data
        {
            "success": true,
            "message": "Comment created successfully.",
            "payload": {
                "id": 5,
                "article": 2,
                "commenter": "adminuser@yopmail.com",
                "body": "comment1",
                "created_at": "2024-12-23T00:44:43.193034",
                "updated_at": "2024-12-23T00:44:43.193052"
            }
        }

    # RetrieveComments : API for get list of comment with pagination and filter
    - `http://localhost:8000/api/articles/2/comments/?commenter__username=adminuser&page=1&page_size=1`

    ## Success Response Data
        {
            "success": true,
            "message": "Comments retrieved successfully.",
            "payload": {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 1,
                        "article": 2,
                        "commenter": "adminuser@yopmail.com",
                        "body": "comment1",
                        "created_at": "2024-12-22T19:23:28.278966",
                        "updated_at": "2024-12-22T19:23:28.278984"
                    }
                ]
            }
        }
        
    # GetComment : API for get comment by id.
    - `http://localhost:8000/api/comments/1/`

    ## Success Response Data
        {
            "success": true,
            "message": "Comment retrieved successfully.",
            "payload": {
                "id": 1,
                "article": 2,
                "commenter": "adminuser@yopmail.com",
                "body": "comment1",
                "created_at": "2024-12-22T19:23:28.278966",
                "updated_at": "2024-12-22T19:23:28.278984"
            }
        }
        
    # UpdateComment : API for update comment.
    - `http://localhost:8000/api/comments/5/`

    ## Success Response Data
        {
            "success": true,
            "message": "Comment updated successfully.",
            "payload": {
                "id": 5,
                "article": 2,
                "commenter": "adminuser@yopmail.com",
                "body": "comment2",
                "created_at": "2024-12-23T00:44:43.193034",
                "updated_at": "2024-12-23T00:45:30.177779"
            }
        }
        
    # DeleteComment : API for delete comment.
    - `http://localhost:8000/api/comments/5/`

    ## Success Response Data
        {
            "success": true,
            "message": "Comment deleted successfully."
        }
    """
