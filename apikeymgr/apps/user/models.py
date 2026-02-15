from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
import random


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email not provided"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields["is_staff"] is not True:
            raise ValueError(_("Make sure to give superuser is_staff = True"))
        if extra_fields["is_superuser"] is not True:
            raise ValueError(_("Make sure to give superuser is_superuser = True"))
        if extra_fields["is_active"] is not True:
            raise ValueError(_("Make sure to give superuser is_active = True"))

        return self.create_user(email, password, **extra_fields)


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
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(_("Email address"), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default=PLAN_FREE)

    is_suspended = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username if self.username else self.email

    def save(self, *args, **kwargs):
        # auth generate username for reg users
        # first part of email before @ + random 4 digit numbers from 0001-9999
        if not self.is_superuser or not self.is_staff:
            self.username = self.email.split("@")[0] + f"{random.randint(1, 9999):04}"
        return super(User, self).save(*args, **kwargs)
