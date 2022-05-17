from django.db import models
from django.contrib.postgres.fields import ArrayField

import uuid

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    class Meta:
        abstract = True


class Medicine(BaseModel):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    composition = ArrayField(
        models.CharField(max_length=20),
        size=5
    )
    expiration = models.IntegerField() # IN MONTHS
    cost = models.FloatField()
    searchable = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name