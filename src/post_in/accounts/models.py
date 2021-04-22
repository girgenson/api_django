from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import (EmailField, CharField, BooleanField, DateTimeField, )


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, first_name=None, last_name=None,
                     is_active=None, is_staff=None, is_admin=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('Нужно ввести имейл')
        if not password:
            raise ValueError('Нужно ввести пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.is_staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255)
    first_name = CharField(max_length=255, blank=True, null=True)
    last_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=False)
    admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager

