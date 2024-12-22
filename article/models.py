from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    """
    User manager class to handle user creation
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a new User
          - Normalizes the email
          - Also creates a new auth token for the user
        """

        if not email:
            raise ValueError("User must have a valid email")

        email = self.normalize_email(email)

        # Set default role if not provided
        if "role" not in extra_fields:
            extra_fields["role"] = Role.VIEWER  # Set default role as VIEWER

        user = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save()

        # Optionally create a token here (if using a token system)
        # Token.objects.create(user=user)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates a superuser
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Role(models.TextChoices):
    ADMIN = "admin", _("Admin")
    AUTHOR = "author", _("Author")
    VIEWER = "viewer", _("Viewer")


class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
    )
    email = models.EmailField(unique=True)
    is_delete = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="article_user",
    )
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.title)


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_comments"
    )
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user"
    )
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
