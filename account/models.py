from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('User should have an phone_number')
        if not password:
            raise ValueError('User should have a password')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'phone_number'
    email = models.EmailField(verbose_name=_('Email'))
    archive = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, null = True , blank= True , unique = True)
    nationalcode = models.CharField(max_length=12, null = True , blank= True)
    address = models.TextField(blank=True, null=True)
    is_owner = models.BooleanField(default=False, verbose_name=_('Is Owner'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'),null = True , blank= True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'),null = True , blank= True)
    objects = UserManager()

    def __str__(self):
        return self.phone_number


def give_default_username(sender, instance, *args, **kwargs):
    instance.username = instance.phone_number
pre_save.connect(give_default_username, sender=User)