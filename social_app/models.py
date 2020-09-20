from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Supply Email Please")
        if not username:
            raise ValueError("Supply User Name Please")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser):
    email = models.EmailField(max_length=120, unique=True)
    username = models.CharField(max_length=100, unique=True)
    validity = models.CharField(max_length=100)
    clearbit_data = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def is_active(self):
        pass

    def has_module_perms(self, app_label):
        return True

    objects = CustomProfileManager()
