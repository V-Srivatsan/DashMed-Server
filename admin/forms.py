from django import forms
from utils import Validators


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(validators=Validators.PASSWORD)



class GetUserForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    username = forms.CharField(max_length=15)

class UpdateUserForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    user_id = forms.CharField(validators=Validators.UID)
    password = forms.CharField(validators=Validators.PASSWORD)



class GetWarehousesForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    name = forms.CharField(max_length=30)

class AddWarehouseForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    username = forms.CharField(max_length=15)
    password = forms.CharField(validators=Validators.PASSWORD)
    name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=150)
    lat = forms.FloatField()
    long = forms.FloatField()

class UpdateWarehouseForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    warehouse_id = forms.CharField(validators=Validators.UID)
    name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=150)
    lat = forms.FloatField()
    long = forms.FloatField()

class RemoveWarehouseForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    warehouse_id = forms.CharField(validators=Validators.UID)



class GetMedicinesForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)

class AddMedicineForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=500)
    expiration = forms.IntegerField()
    cost = forms.FloatField()

class UpdateMedicineForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    med_id = forms.CharField(validators=Validators.UID)
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=500)
    expiration = forms.IntegerField()
    cost = forms.FloatField()
    searchable = forms.BooleanField()



class PasswordForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    password = forms.CharField(validators=Validators.PASSWORD)