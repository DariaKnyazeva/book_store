from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.utils import timezone


class UserRole:
    CUSTOMER = 1
    STORE_OWNER = 2


class UserManager(DjangoUserManager):
    def create_user(self, username, user_role=UserRole.CUSTOMER, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        By default creates Customer user
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, user_role=user_role)

        user.set_password(password)
        # user.user_role = user_role
        user.save(using=self._db)
        return user

    def create_customer(self, username, email=None, password=None):
        return self.create_user(username, email=email, password=password)

    def create_store_owner(self, username, email=None, password=None):
        return self.create_user(username, user_role=UserRole.STORE_OWNER, email=email, password=password)


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        (UserRole.CUSTOMER, 'Customer'),
        (UserRole.STORE_OWNER, 'Store Owner'),
    )
    user_role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES)

    objects = UserManager()

    @property
    def is_customer(self):
        return self.user_role == UserRole.CUSTOMER
