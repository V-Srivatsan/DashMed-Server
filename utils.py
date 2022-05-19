from django.contrib.gis.geos import Point
from django.forms import Form as Dj_Form

from warehouse.models import Warehouse
from misc.models import Medicine



def addWarehouse(
    username: str,
    password: str,
    name: str,
    address: str,
    coords: tuple
):
    try:
        warehouse = Warehouse(
            username=username,
            password=password,
            name=name,
            address=address,
            coords=Point(coords[1], coords[0])
        )
        warehouse.save()
        return warehouse.id.hex
    except Exception:
        return False


def addMedicine(
    name: str,
    description: str,
    composition: list,
    expiration: int,
    cost: float
):
    med = Medicine(
        name=name,
        description=description,
        composition=composition,
        expiration=expiration,
        cost=cost
    )
    med.save()
    return med.id.hex





# HELPER FUNCTIONS AND CLASSES

from django.core.validators import RegexValidator
import re


def getData(data: dict, Form: Dj_Form):
    form = Form(data)
    if form.is_valid():
        return True, form.cleaned_data
    return False, {
        'valid': False,
        'message': Messages.INVALID_DATA
    }


def regexValidate(validate_str: str, pattern: str):
    regex = re.compile(pattern)
    return bool(regex.fullmatch(validate_str))



class Patterns:
    UID = '[0-9a-f]{32}'
    PASSWORD = '.{4,}[0-9]{1,}'


class Validators:
    UID = [RegexValidator(Patterns.UID)]
    PASSWORD = [RegexValidator(Patterns.PASSWORD)]


class Messages:
    INVALID_USERNAME = 'This username does not exist! Please check your credentials!'
    INCORRECT_PASSWORD = 'The password is incorrect! Please try again!'
    USERNAME_TAKEN = 'This username is already taken! Try another!'

    INVALID_DATA = 'This action was not valid! Please try again!'
    ORDER_NOT_FOUND = 'The order was not found! Please try again!'

    AUTH_ERROR = 'Authentication failed! Please try reinstalling the app!'
    EMP_ERROR = 'Employee not found! Please try again!'
    USER_ERROR = 'User was not found! Please try again!'