
from django.contrib.auth import models as auth_model
from django.contrib.auth.models import UserManager
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)
from django.db import models


class UserModel(auth_model.AbstractBaseUser, auth_model.PermissionsMixin):
    USERNAME_MIN_LENGTH = 1
    USERNAME_MAX_LENGTH = 255
    USERNAME_VERBOSE_NAME = "Потребителско име"
    PASSWORD_VERBOSE_NAME = "Парола"
    PERSONAL_NUMBER_MIN_VALUE = 700000
    PERSONAL_NUMBER_MAX_VALUE = 800000
    PERSONAL_NUMBER_FIRST_INT = [
        7,
    ]  # must be list with integers
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 255
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 255
    PASSWORD_MAX_LENGTH = 255

    username = models.CharField(
        verbose_name=USERNAME_VERBOSE_NAME,
        max_length=USERNAME_MAX_LENGTH,
        validators=(MinLengthValidator(USERNAME_MIN_LENGTH),),
        unique=True,
    )
    personal_number = models.PositiveIntegerField(
        validators=(
            MinValueValidator(PERSONAL_NUMBER_MIN_VALUE),
            MaxValueValidator(PERSONAL_NUMBER_MAX_VALUE),

        ),
        unique=True,
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(MinLengthValidator(FIRST_NAME_MIN_LENGTH),),
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(MinLengthValidator(LAST_NAME_MIN_LENGTH),),
    )
    email = models.EmailField(
        default=None,
        null=True,
        blank=True,
    )
    password = models.CharField(
        verbose_name=PASSWORD_VERBOSE_NAME,
        max_length=PASSWORD_MAX_LENGTH,
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_superuser = models.BooleanField(
        default=False,
    )

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    object = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.get_full_name
