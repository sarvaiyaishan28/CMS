from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.views import (
    ArticleViewSet,
    CommentViewSet,
    LoginViewSet,
    RegisterViewSet,
    UserViewSet,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register("register", RegisterViewSet, basename="register")
router.register("login", LoginViewSet, basename="login")
router.register("users", UserViewSet, basename="users")
router.register("articles", ArticleViewSet, basename="article")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "articles/<int:article_id>/comments/",
        CommentViewSet.as_view({"post": "create", "get": "list"}),
        name="article-comments",
    ),
    path(
        "comments/<int:pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="comment-detail",
    ),
]
