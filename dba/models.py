from django.db import models
from django.contrib.auth.hashers import make_password, check_password as dj_check

from misc.models import BaseModel


# Create your models here.
class Admin(BaseModel):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=88)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Admin, self).save(*args, **kwargs)

    def check_password(self, password_check: str) -> bool:
        return dj_check(password_check, self.password)
