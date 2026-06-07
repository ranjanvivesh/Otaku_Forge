"""
Fixed accounts/models.py - Corrected User model for Django admin compatibility

This version uses Django's built-in AbstractBaseUser password field
and includes PermissionsMixin for proper permission handling.

Installation:
1. Replace the content of your accounts/models.py with this file
2. Run: python manage.py makemigrations
3. Run: python manage.py migrate
4. Run: python manage.py createsuperuser
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password as django_check_password


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not name:
            raise ValueError("Users must have a name.")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, name=name)
        # set_password() automatically hashes and stores in the 'password' field
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password)
        user.is_superuser = True
        user.is_admin = True
        user.is_email_verified = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as the unique identifier.
    
    Uses Django's built-in AbstractBaseUser which provides:
    - password field (hashed automatically)
    - last_login field
    - is_active field
    - Basic authentication methods (set_password, check_password)
    
    Added PermissionsMixin for:
    - is_superuser field
    - Groups and permissions support
    """

    email = models.CharField(
        max_length=255,
        unique=True,
        help_text="User's email address (login identifier)"
    )
    name = models.CharField(max_length=200)
    
    # OAuth integration (optional)
    google_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Google OAuth ID if user signed up via Google"
    )
    
    is_email_verified = models.BooleanField(
        default=False,
        help_text="Whether the user has verified their email via OTP"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the user account is active"
    )
    is_admin = models.BooleanField(
        default=False,
        help_text="Whether the user has admin privileges"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """Required by Django admin — staff users can access admin panel"""
        return self.is_admin


class OTPRecord(models.Model):
    """
    Temporary OTP records for email verification during registration.
    """
    
    email = models.EmailField(
        help_text="Email address awaiting verification"
    )
    otp_hash = models.CharField(
        max_length=64,
        help_text="Hashed OTP value"
    )
    expires_at = models.DateTimeField(
        help_text="When this OTP expires"
    )
    pending_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name from registration form (pending verification)"
    )
    pending_password = models.CharField(
        max_length=255,
        blank=True,
        help_text="Hashed password from registration form (pending verification)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "OTP Record"
        verbose_name_plural = "OTP Records"
        unique_together = [("email",)]
        indexes = [models.Index(fields=["email"])]

    def __str__(self):
        return f"OTP for {self.email}"