# External Import
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for User"""

    def get_by_natural_key(self, username):
        """
        This takes username/email case insensitive while performing login operation
        """
        return self.get(**{self.model.USERNAME_FIELD + '__iexact': username})

    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, username and password.
        """

        # Username and email validation while creating new user
        if username is None:
            raise ValueError('User must have a username')
        if email is None:
            raise ValueError('User must have a Email')

        # Normalizing email my removing extra spaces
        email = self.normalize_email(email)

        # Assigning username & Email to the variable user
        user = self.model(username=username, email=email)

        # Setting Password with encryption
        user.set_password(password)

        # Storing the user data to the databaase
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        if password is None:
            raise ValueError('Password should not be none')

        # Creating user with the help above create_user function
        user = self.create_user(username, email, password)

        # Assigning critical fields value as True for the superuser
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True

        # Saving modified superuser to the database
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""

    # Adding Email Field
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    # Adding is_business & is_customer field to identify business and customer
    is_business = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    # These filed are porvided as default by Django
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    # Configuring UserManager to the User Model
    objects = UserManager()
    USERNAME_FIELD = 'username'
    # Email is marked as required fields means it cannot be null
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        """Return string representation of the user's username & email"""
        return f'{self.username}'

    @property
    def active(self):
        return self.is_active
