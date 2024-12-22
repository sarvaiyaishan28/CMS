from django.contrib import admin
from article.forms import UserChangeForm, UserCreationForm
from .models import User, Article, Comment
from django.contrib.auth import admin as auth_admin

# Register your models here.
ModelField = lambda model: type(
    "Subclass" + model.__name__,
    (admin.ModelAdmin,),
    {
        "list_display": [x.name for x in model._meta.fields],
        "search_fields": [x.name for x in model._meta.fields],
        "list_filter": [x.name for x in model._meta.fields],
    },
)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_delete",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "id",
        "email",
        "username",
        "role",
        "is_active",
        "is_delete",
        "last_login",
        "date_joined",
    ]
    search_fields = ["username", "email"]
    ordering = ["-id"]


admin.site.register(Article, ModelField(Article))
admin.site.register(Comment, ModelField(Comment))
