from django.db import models
from django.contrib.auth.models import AbstractUser
from api.manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True,)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def name(self):
        return self.first_name + " " + self.last_name
    
    def __str__(self) :
        return self.email