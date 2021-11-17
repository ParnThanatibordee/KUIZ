from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class MyAccountManager(BaseUserManager):
    def check_no_input(self, email, username, first_name, last_name, password):
        if not email:
            raise ValueError("Users must have an Email")
        if not username:
            raise ValueError("Users must have a Username")

    def create_user(self, email, username, first_name='', last_name='', password=None):
        self.check_no_input(email, username, first_name, last_name, password)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        self.check_no_input(email, username, first_name, last_name, password, )
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='profiles', default='profile-pic.png', blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password','is_teacher']
    objects = MyAccountManager()

    def __str__(self):
        return F"{self.username}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
