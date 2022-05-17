from django.db import models
from django.contrib.auth.hashers import make_password, check_password as dj_check

from misc.models import BaseModel
from warehouse.models import Warehouse

# Create your models here.
class Employee(BaseModel):
    warehouse = models.ForeignKey(to=Warehouse, on_delete=models.CASCADE)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=88)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Employee, self).save(*args, **kwargs)

    def check_password(self, password: str):
        return dj_check(password, self.password)

    def __str__(self) -> str:
        return f'{self.username}'