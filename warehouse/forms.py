from django import forms
from utils import Validators


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(validators=Validators.PASSWORD)


class AddEmployeeForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)
    username = forms.CharField(max_length=15)
    password = forms.CharField(validators=Validators.PASSWORD)

class UpdateEmployeeForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    emp_uid = forms.CharField(validators=Validators.UID)
    name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)

class RemoveEmployeeForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    emp_uid = forms.CharField(validators=Validators.UID)


class EntryForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    date = forms.DateField()


class AddItemForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    med_id = forms.CharField(validators=Validators.UID)
    manufactured = forms.DateField()
    quantity = forms.IntegerField()

class UpdateItemForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    item_id = forms.CharField(validators=Validators.UID)
    manufactured = forms.DateField()
    quantity = forms.IntegerField()

class RemoveItemForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    item_id = forms.CharField(validators=Validators.UID)


class UpdatePasswordForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    password = forms.CharField(validators=Validators.PASSWORD)


class AuthForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
