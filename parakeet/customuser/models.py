from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from plan.models import Plan


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        user = User.objects.get(email=email)
        user.user_permissions.clear()
        # permission = Permission.objects.get(codename='view_permission')
        # user.user_permissions.add(permission)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        plan = Plan.objects.all()
        extra_fields.setdefault("plan_id", plan[0])

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    plan_id = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=30)
    family_name = models.CharField(max_length=100)
    given_name = models.CharField(max_length=100)
    mail_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=300)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
