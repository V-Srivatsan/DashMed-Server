from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.auth.hashers import make_password, check_password as dj_check

from misc.models import Medicine, BaseModel
import datetime

# Create your models here.
class Warehouse(BaseModel):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=88)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=150)
    coords = PointField()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Warehouse, self).save(*args, **kwargs)

    def check_password(self, password: str):
        return dj_check(password, self.password)

    def __str__(self) -> str:
        return self.name


from employee.models import Employee

class Entry(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE)
    date = models.DateField()


class Item(BaseModel):
    warehouse = models.ForeignKey(to=Warehouse, on_delete=models.CASCADE)
    medicine = models.ForeignKey(to=Medicine, on_delete=models.CASCADE)
    manufactured = models.DateField()
    quantity = models.IntegerField()

    def hasExpired(self) -> bool:
        total_months = self.manufactured.month + self.medicine.expiration
        months = total_months % 12
        delta_years = (total_months - months) // 12
        return datetime.datetime.today().date() > datetime.date(self.manufactured.year + delta_years, months, self.manufactured.day)
    