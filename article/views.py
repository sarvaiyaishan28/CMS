from CMS.pagination import CustomPagination
from api_document.doc import (
    ARTICLE_DOCS,
    COMMENT_DOCS,
    LOGIN_DOCS,
    REGISTER_DOCS,
    USER_DOCS,
)
from article.models import Article, Comment, Role, User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ArticleSerializer,
    CommentSerializer,
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterViewSet(ModelViewSet):
    __doc__ = REGISTER_DOCS
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    http_method_names = ["post"]
    queryset = User.objects.all()

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        role = serializer.validated_data["role"]
        username = serializer.validated_data["username"]
        email = serializer.validated_data.get("email", None)
        password = serializer.validated_data["password"]
        first_name = serializer.validated_data.get("first_name", None)
        last_name = serializer.validated_data.get("last_name", None)

        if email is None:
            return Response(
                {
                    "success": False,
                    "message": "Email is required, please enter valid email.",
                    "payload": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()
        if user is not None:
            return Response(
                {
                    "success": False,
                    "message": f"{email} is already registered, please try different email.",
                    "payload": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=Role[role.upper()].value,
        )
        create_user.set_password(password)
        create_user.save()

        serializer = UserSerializer(create_user)
        return Response(
            {
                "success": True,
                "message": "User created successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginViewSet(ModelViewSet):
    __doc__ = LOGIN_DOCS
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    http_method_names = ["post"]
    queryset = User.objects.all()

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email", None)
        password = serializer.validated_data["password"]

        if not email or not password:
            return Response(
                {"success": False, "message": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {"success": False, "message": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"success": False, "message": "Your account is disabled."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        user_data = UserSerializer(user).data
        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "payload": {
                    "user": user_data,
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )


class UserViewSet(ModelViewSet):
    __doc__ = USER_DOCS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
    ]
    filterset_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
    ]
    pagination_class = CustomPagination
    serializer_class = UserSerializer
    http_method_names = ["get", "put", "delete"]
    queryset = User.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to access this. Only admins are allowed.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        queryset = self.get_queryset()
        filter_queryset = self.filter_queryset(queryset)
        paginate_queryset = self.paginate_queryset(filter_queryset)
        serializer = self.get_serializer(paginate_queryset, many=True)
        payload = self.get_paginated_response(serializer.data)
        return Response(
            {
                "success": True,
                "message": "Users list fetched successfully.",
                "payload": payload,
            }
        )

    def retrieve(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to access this. Only admins are allowed.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(
            {
                "success": True,
                "message": "User retrieved successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        # Check if the user is allowed to update the details
        if request.user != user and request.user.role != "admin":
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to update this user.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Perform the update
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "User details updated successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # Check if the user is allowed to delete
        if request.user.role != "admin":
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to delete this user. Only admins can delete users.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user.delete()

        return Response(
            {
                "success": True,
                "message": "User deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class ArticleViewSet(ModelViewSet):
    __doc__ = ARTICLE_DOCS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        "author__username",
        "author__email",
        "title",
        "body",
        "author__role",
        "published",
    ]
    filterset_fields = [
        "author__username",
        "author__email",
        "title",
        "body",
        "author__role",
        "published",
    ]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "patch", "put", "delete"]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_queryset = self.filter_queryset(queryset)
        paginate_queryset = self.paginate_queryset(filter_queryset)
        serializer = self.get_serializer(paginate_queryset, many=True)
        payload = self.get_paginated_response(serializer.data)
        return Response(
            {
                "success": True,
                "message": "Articles retrieved successfully.",
                "payload": payload,
            },
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.get_serializer(article)
        return Response(
            {
                "success": True,
                "message": "Article retrieved successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.role not in ["admin", "author"]:
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to create article.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer.save(author=request.user)
        return Response(
            {
                "success": True,
                "message": "Article created successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="publish",
        permission_classes=[IsAuthenticated],
    )
    def publish_article(self, request, pk=None):
        article = self.get_object()

        if request.user.role != "admin":
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to publish/unpublish this article.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        is_published = request.data.get("is_published")

        if is_published is None or not isinstance(is_published, bool):
            return Response(
                {
                    "success": False,
                    "message": "'is_published' parameter must be a boolean value (true/false).",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        article.published = is_published
        article.save()

        action_message = "published" if is_published else "unpublished"
        serializer = ArticleSerializer(article)
        return Response(
            {
                "success": True,
                "message": f"Article successfully {action_message}.",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        article = self.get_object()

        # Only Admins or the author of the article can edit
        if request.user.role not in ["admin", "author"]:
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to edit articles.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.user.role == "author" and article.author != request.user:
            return Response(
                {
                    "success": False,
                    "message": "You can only edit your own articles.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(article, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Article updated successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        if request.user.role == "admin" or article.author == request.user:
            article.delete()
            return Response(
                {"success": True, "message": "Article deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {
                "success": False,
                "message": "You do not have permission to delete this article.",
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class CommentViewSet(ModelViewSet):
    __doc__ = COMMENT_DOCS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        "body",
        "article__title",
        "commenter__username",
        "body",
    ]
    filterset_fields = [
        "article__title",
        "commenter__username",
        "body",
    ]
    pagination_class = CustomPagination
    http_method_names = ["post", "get", "delete", "patch"]
    queryset = Comment.objects.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        article_id = self.kwargs.get("article_id")
        print(f"article_id : {article_id}")
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response(
                {"success": False, "message": "Article not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(commenter=request.user, article=article)
        return Response(
            {
                "success": True,
                "message": "Comment created successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        article_id = self.kwargs.get("article_id")
        if not article_id:
            return Response(
                {"success": False, "message": "'article_id' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment = self.filter_queryset(Comment.objects.filter(article_id=article_id))
        comments = self.paginate_queryset(comment)
        serializer = self.get_serializer(comments, many=True)
        payload = self.get_paginated_response(serializer.data)
        return Response(
            {
                "success": True,
                "message": "Comments retrieved successfully.",
                "payload": payload,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.commenter and request.user.role != "admin":
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to update this comment.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Comment updated successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user.role == "admin" or comment.commenter == request.user:
            comment.delete()
            return Response(
                {"success": True, "message": "Comment deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {
                "success": False,
                "message": "You do not have permission to delete this comment.",
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    def retrieve(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response(
            {
                "success": True,
                "message": "Comment retrieved successfully.",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
