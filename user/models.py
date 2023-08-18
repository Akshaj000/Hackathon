from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    id = models.AutoField(primary_key=True),

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    name = models.CharField(
        max_length=100,
        blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True, null=True
    )

    is_banned = models.BooleanField(default=False)
    meta = models.JSONField(default=dict)

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


__all__ = [
    'User',
]
