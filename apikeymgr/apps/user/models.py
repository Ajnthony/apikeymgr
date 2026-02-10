from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, pw=None, **extra_fields):
        if not email:
            raise ValueError(_("Email not provided"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(pw)
        user.save()

        return user

    def create_superuser(self, email, pw=None, **extra_fields):
        extra_fields.set_default("is_superuser", True)
        extra_fields.set_default("is_staff", True)
        extra_fields.set_default("is_active", True)

        superuser = self.create_user(email, pw, **extra_fields)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    PLAN_FREE = "free"
    PLAN_PRO = "pro"

    PLAN_CHOICES = (
        (PLAN_FREE, "free"),
        (PLAN_PRO, "pro"),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    full_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    email = models.EmailField(_("Email address"), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_suspended = models.BooleanField(default=False)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default=PLAN_FREE)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username if self.username else self.email
