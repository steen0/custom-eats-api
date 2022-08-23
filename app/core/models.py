from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import gettext as _


# ------------------ DEFINE MANAGERS ------------------
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address cannot be blank')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def upgrade_user(self, email):
        user = User.objects.get(email=email)
        if not user:
            raise ObjectDoesNotExist
        if not user.password:
            user.password = 'admin'
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# ------------------ DEFINE MODELS ------------------
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Order(models.Model):

    class OrderType(models.TextChoices):
        ONE_TIME = 'one_time', _('One-Time')
        RECURRING_WEEKLY = 'recurring_weekly', _('Recurring Weekly')
        RECURRING_MONTHLY = 'recurring_monthly', _('Recurring Monthly')
        RECURRING_YEARLY = 'recurring_yearly', _('Recurring Yearly')

    class OrderStatus(models.TextChoices):
        PROCESSING = 'processing', _('Processing')
        COMPLETED = 'completed', _('Completed')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    order_type = models.CharField(
        choices=OrderType.choices,
        blank=False,
        max_length=40,
    )
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING,
        max_length=10,
    )
