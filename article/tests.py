from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from article.models import Article, Comment, User
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up test data. Create users with different roles.
        """
        self.admin_user = get_user_model().objects.create_user(
            email="admin@example.com",
            password="adminpass",
            role="admin",
            username="adminexample",
        )
        self.viewer_user = get_user_model().objects.create_user(
            email="viewer@example.com",
            password="viewerpass",
            role="viewer",
            username="viewerexample",
        )
        self.author_user = get_user_model().objects.create_user(
            email="author@example.com",
            password="authorpass",
            role="author",
            username="authorexample",
        )

        # Create an authentication token for the users
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.viewer_token = str(RefreshToken.for_user(self.viewer_user).access_token)
        self.author_token = str(RefreshToken.for_user(self.author_user).access_token)

    def test_user_can_update_their_own_details(self):
        """
        Test that a user can update their own details.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.author_token)
        updated_data = {
            "email": "updated_author@example.com",
            "first_name": "Updated",
            "last_name": "User",
        }
        url = f"/api/users/{self.author_user.id}/"
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author_user.refresh_from_db()
        self.assertEqual(self.author_user.email, "updated_author@example.com")
        self.assertEqual(self.author_user.first_name, "Updated")
        self.assertEqual(self.author_user.last_name, "User")

    def test_user_cannot_update_others_details(self):
        """
        Test that a user cannot update another user's details.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.author_token)
        updated_data = {"email": "unauthorized_update@example.com"}
        url = f"/api/users/{self.viewer_user.id}/"
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"], "You do not have permission to update this user."
        )

    def test_list_users_with_pagination(self):
        """
        Test that the user list view supports pagination.
        """
        url = "/api/users/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.admin_token)
        response = self.client.get(url, {"page_size": 1})
        self.assertEqual(len(response.data["payload"]["results"]), 1)

    def test_search_users_by_username(self):
        """
        Test that users can be searched by their username.
        """
        url = "/api/users/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.admin_token)
        response = self.client.get(url, {"search": "authorexample"})
        self.assertEqual(len(response.data["payload"]["results"]), 1)

    def test_filter_users_by_role(self):
        """
        Test that users can be filtered by their role.
        """
        url = "/api/users/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.admin_token)
        response = self.client.get(url, {"role": "author", "page_size": 1})
        self.assertEqual(len(response.data["payload"]["results"]), 1)

    def test_update_user_as_admin(self):
        """
        Test that admins can update user details.
        """
        url = f"/api/users/{self.viewer_user.id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.admin_token)
        response = self.client.put(url, data={"email": "updated_email@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "User details updated successfully.")
        self.viewer_user.refresh_from_db()
        self.assertEqual(self.viewer_user.email, "updated_email@example.com")

    def test_update_user_as_non_admin(self):
        """
        Test that non-admin users cannot update another user's details.
        """
        url = f"/api/users/{self.admin_user.id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.viewer_token)
        response = self.client.put(url, data={"email": "updated_email@example.com"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"], "You do not have permission to update this user."
        )

    def test_destroy_user_as_admin(self):
        """
        Test that admins can delete a user.
        """
        url = f"/api/users/{self.author_user.id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.admin_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "User deleted successfully.")
        self.assertFalse(
            get_user_model().objects.filter(id=self.author_user.id).exists()
        )

    def test_destroy_user_as_non_admin(self):
        """
        Test that non-admin users cannot delete users.
        """
        url = f"/api/users/{self.admin_user.id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.viewer_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"],
            "You do not have permission to delete this user. Only admins can delete users.",
        )


class ArticleViewSetTestCase(APITestCase):

    def setUp(self):
        """
        Set up test data including users and articles.
        """
        self.client = APIClient()

        # Create test users
        self.admin_user = get_user_model().objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword",
            role="admin",
        )
        self.author_user = get_user_model().objects.create_user(
            username="authoruser",
            email="author@example.com",
            password="authorpassword",
            role="author",
        )
        self.viewer_user = get_user_model().objects.create_user(
            username="vieweruser",
            email="viewer@example.com",
            password="viewpassword",
            role="viewer",
        )

        # Create articles
        self.article1 = Article.objects.create(
            title="Article 1",
            body="This is article 1",
            author=self.author_user,
            published=False,
        )
        self.article2 = Article.objects.create(
            title="Article 2",
            body="This is article 2",
            author=self.author_user,
            published=True,
        )

    def authenticate(self, user):
        """
        Helper method to authenticate users.
        """
        self.client.force_authenticate(user=user)

    def test_list_articles_with_pagination(self):
        """
        Test that the articles list view supports pagination.
        """
        url = "/api/articles/"
        self.authenticate(self.admin_user)
        response = self.client.get(url, {"page_size": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)

    def test_create_article_with_valid_permissions(self):
        """
        Test that an admin or author can create an article.
        """
        url = "/api/articles/"
        self.authenticate(self.author_user)
        data = {
            "title": "New Article",
            "body": "This is a new article.",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Article created successfully.")

    def test_create_article_with_invalid_permissions(self):
        """
        Test that a viewer cannot create an article.
        """
        url = "/api/articles/"
        self.authenticate(self.viewer_user)
        data = {
            "title": "New Article",
            "body": "This is a new article.",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"], "You do not have permission to create article."
        )

    def test_update_article_with_valid_permissions(self):
        """
        Test that an admin or the author can update an article.
        """
        url = f"/api/articles/{self.article1.id}/"
        self.authenticate(self.author_user)
        data = {"title": "Updated Article 1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Article updated successfully.")

    def test_update_article_with_invalid_permissions(self):
        """
        Test that a viewer cannot update an article.
        """
        url = f"/api/articles/{self.article1.id}/"
        self.authenticate(self.viewer_user)
        data = {"title": "Updated Article 1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"], "You do not have permission to edit articles."
        )

    def test_publish_article_with_valid_permissions(self):
        """
        Test that an admin can publish/unpublish an article.
        """
        url = f"/api/articles/{self.article1.id}/publish/"
        self.authenticate(self.admin_user)
        data = {"is_published": True}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["payload"]["published"])

    def test_publish_article_with_invalid_permissions(self):
        """
        Test that a non-admin user cannot publish/unpublish an article.
        """
        url = f"/api/articles/{self.article1.id}/publish/"
        self.authenticate(self.author_user)
        data = {"is_published": True}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"],
            "You do not have permission to publish/unpublish this article.",
        )

    def test_delete_article_with_valid_permissions(self):
        """
        Test that an admin or author can delete an article.
        """
        url = f"/api/articles/{self.article1.id}/"
        self.authenticate(self.author_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "Article deleted successfully.")

    def test_delete_article_with_invalid_permissions(self):
        """
        Test that a viewer cannot delete an article.
        """
        url = f"/api/articles/{self.article1.id}/"
        self.authenticate(self.viewer_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"],
            "You do not have permission to delete this article.",
        )


class CommentViewSetTestCase(APITestCase):

    def setUp(self):
        """
        Set up test data including users, articles, and comments.
        """
        self.client = APIClient()

        # Create test users
        self.admin_user = get_user_model().objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword",
            role="admin",
        )
        self.author_user = get_user_model().objects.create_user(
            username="authoruser",
            email="author@example.com",
            password="authorpassword",
            role="author",
        )
        self.viewer_user = get_user_model().objects.create_user(
            username="vieweruser",
            email="viewer@example.com",
            password="viewpassword",
            role="viewer",
        )

        # Create articles
        self.article1 = Article.objects.create(
            title="Article 1",
            body="This is article 1",
            author=self.author_user,
            published=True,
        )
        self.article2 = Article.objects.create(
            title="Article 2",
            body="This is article 2",
            author=self.author_user,
            published=True,
        )

        # Create comments
        self.comment1 = Comment.objects.create(
            body="This is a comment on article 1",
            article=self.article1,
            commenter=self.author_user,
        )
        self.comment2 = Comment.objects.create(
            body="This is a comment on article 2",
            article=self.article2,
            commenter=self.viewer_user,
        )

    def authenticate(self, user):
        """
        Helper method to authenticate users.
        """
        self.client.force_authenticate(user=user)

    def test_list_comments_with_pagination(self):
        """
        Test that the comments list view supports pagination.
        """
        url = f"/api/articles/{self.article1.id}/comments/"
        self.authenticate(self.admin_user)
        response = self.client.get(url, {"page_size": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)

    def test_create_comment_with_valid_permissions(self):
        """
        Test that a logged-in user (author, admin, or viewer) can create a comment.
        """
        url = f"/api/articles/{self.article1.id}/comments/"
        self.authenticate(self.viewer_user)
        data = {"body": "This is a new comment."}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Comment created successfully.")
        self.assertEqual(response.data["payload"]["body"], "This is a new comment.")

    def test_create_comment_with_invalid_article(self):
        """
        Test that attempting to create a comment on a non-existent article returns a 404 error.
        """
        url = "/api/articles/999/comments/"
        self.authenticate(self.viewer_user)
        data = {"body": "This comment is on a non-existent article."}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Article not found.")

    def test_update_comment_with_valid_permissions(self):
        """
        Test that an admin or the author can update a comment.
        """
        url = f"/api/comments/{self.comment1.id}/"
        self.authenticate(self.author_user)
        data = {"body": "Updated comment text"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Comment updated successfully.")
        self.assertEqual(response.data["payload"]["body"], "Updated comment text")

    def test_update_comment_with_invalid_permissions(self):
        """
        Test that a viewer cannot update a comment they did not create.
        """
        url = f"/api/comments/{self.comment1.id}/"
        self.authenticate(self.viewer_user)
        data = {"body": "Attempted update by viewer"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"],
            "You do not have permission to update this comment.",
        )

    def test_delete_comment_with_valid_permissions(self):
        """
        Test that an admin or the author can delete a comment.
        """
        url = f"/api/comments/{self.comment1.id}/"
        self.authenticate(self.author_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "Comment deleted successfully.")

    def test_delete_comment_with_invalid_permissions(self):
        """
        Test that a viewer cannot delete a comment they did not create.
        """
        url = f"/api/comments/{self.comment1.id}/"
        self.authenticate(self.viewer_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"],
            "You do not have permission to delete this comment.",
        )

    def test_list_comments_for_non_existent_article(self):
        """
        Test that attempting to list comments for a non-existent article returns a 404 error.
        """
        url = "/api/articles/999/comments/"
        self.authenticate(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_with_missing_body(self):
        """
        Test that trying to create a comment without a body returns a validation error.
        """
        url = f"/api/articles/{self.article1.id}/comments/"
        self.authenticate(self.viewer_user)
        data = {}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["body"][0], "This field is required.")
