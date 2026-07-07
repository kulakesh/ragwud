from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):

        if not username:
            raise ValueError("Username is required")

        user = self.model(
            username=username,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None, **extra_fields):

        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            username,
            password,
            **extra_fields
        )



class CustomUser( AbstractBaseUser, PermissionsMixin ):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        # ('member', 'Member'),
    )

    username = models.CharField( max_length=100, unique=True )
    name = models.CharField( max_length=100 )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now_add=True )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['role']

    class Meta:
            db_table = 'users'
    def __str__(self):
        return self.username