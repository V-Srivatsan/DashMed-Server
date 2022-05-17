from django import forms
from utils import Validators


class SignupForm(forms.Form):
    name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    username = forms.CharField(max_length=15)
    password = forms.CharField(validators=Validators.PASSWORD)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(validators=Validators.PASSWORD)


class CheckPasswordForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    password = forms.CharField(validators=Validators.PASSWORD)


class UpdateUserForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(validators=Validators.PASSWORD)


class AuthForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)


class GetOrderItemsForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    order_id = forms.CharField(validators=Validators.UID)


class PlaceOrderForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    lat = forms.FloatField()
    long = forms.FloatField()
    address = forms.CharField(max_length=150)

class MedForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    quantity = forms.IntegerField()