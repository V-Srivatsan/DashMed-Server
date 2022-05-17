from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.contrib.gis.db.models.fields import PointField
from django.contrib.auth.hashers import make_password, check_password as dj_check

from misc.models import BaseModel
from warehouse.models import Employee

# Create your models here.
class User(BaseModel):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=88)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def check_password(self, password_check: str) -> bool:
        return dj_check(password_check, self.password)


class Order(BaseModel):

    OPTIONS = (
        ('P', 'Pending'),
        ('C', 'Completed')
    )

    employee = models.ForeignKey(to=Employee, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)

    user_name = models.CharField(max_length=30, null=True)
    user_phone = models.CharField(max_length=15, null=True)
    user_email = models.EmailField(null=True)
    employee_name = models.CharField(max_length=30, null=True)
    employee_phone = models.CharField(max_length=15, null=True)

    items = ArrayField(
        HStoreField(),
        size=20
    )
    coords = PointField()
    order_date = models.DateField(default=datetime.today().date())
    address = models.CharField(max_length=150)
    status = models.CharField(max_length=1, choices=OPTIONS, default='P')

    def save(self, *args, **kwargs):
        self.user_name = self.user.name
        self.user_phone = self.user.phone
        self.user_email = self.user.email

        self.employee_name = self.employee.name
        self.employee_phone = self.employee.phone

        super(Order, self).save(*args, **kwargs)