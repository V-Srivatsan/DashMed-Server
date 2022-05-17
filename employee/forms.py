from django import forms
from utils import Validators


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(validators=Validators.PASSWORD)


class GetPendingOrdersForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)

class GetOrderForm(forms.Form):
    order_id = forms.CharField(validators=Validators.UID)

class DeliverOrderForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    order_id = forms.CharField(validators=Validators.UID)


class PasswordForm(forms.Form):
    uid = forms.CharField(validators=Validators.UID)
    password = forms.CharField(validators=Validators.PASSWORD)
