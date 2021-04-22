from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import (EmailField, CharField, BooleanField, DateTimeField, )


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, first_name=None, last_name=None,
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

    def create_superuser(self, email, password=None, first_name=None, **extra_fields):
        user = self.create_user(email, first_name=first_name, password=password,
                                is_staff=True, is_admin=True)
        return user

    def create_staff_user(self, email, password=None, first_name=None, **extra_fields):
        user = self.create_user(email, first_name=first_name, password=password,
                                is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255)
    first_name = CharField(max_length=255, blank=True, null=True)
    last_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager

    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_last_name(self):
        if self.last_name:
            return self.last_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        print(self.password)
        super().save(*args, **kwargs)

