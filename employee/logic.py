from django.forms import Form as Dj_Form
import uuid

from .forms import *
from utils import Messages, getData

from .models import *
from user.models import *
from misc.models import Medicine



def _getEmployee(uid: str):
    employees = Employee.objects.filter(id=uuid.UUID(uid))
    if len(employees) > 0:
        return employees[0], None
    
    return None, {
        'valid': False,
        'message': Messages.AUTH_ERROR,
    }



def login(req: dict):
    valid, data = getData(req, LoginForm)
    if not valid:
        return data
    
    employees = Employee.objects.filter(username=data['username'])
    if len(employees) == 0:
        return {
            'valid': False,
            'message': 'This username does not exist! Please try again!'
        }

    if not employees[0].check_password(data['password']):
        return {
            'valid': False,
            'message': Messages.INCORRECT_PASSWORD
        }
        
    return {
        'valid': True,
        'message': None,
        'UID': employees[0].id.hex
    }



# ORDERS

def getPendingOrders(req: dict):
    valid, data = getData(req, GetPendingOrdersForm)
    if not valid:
        return data

    employee, res = _getEmployee(data['uid'])
    if res != None:
        return res
    
    return {
        'valid': True,
        'message': None,
        'orders': [{
            'uid': order.id.hex,
            'name': order.user_name,
            'quantity': len(order.items),
        } for order in Order.objects.filter(employee=employee, status='P')]
    }


def getOrder(req: dict):
    valid, data = getData(req, GetOrderForm)
    if not valid:
        return data

    orders = Order.objects.filter(id=uuid.UUID(data['order_id']))
    if len(orders) == 0:
        return {
            'valid': False,
            'message': Messages.ORDER_NOT_FOUND
        }

    order = orders[0]
    coords = order.coords.tuple
    items = []
    for item in order.items:
        medicine: Medicine = Medicine.objects.filter(id=uuid.UUID(item['med_id']))[0]
        items.append({
            'name': medicine.name,
            'description': medicine.description,
            'composition': medicine.composition,
            'expiration': medicine.expiration,
            'cost': medicine.cost,
            'quantity': item['quantity']
        })

    return {
        'valid': True,
        'message': None,
        'name': order.user_name,
        'contact': order.user_phone,
        'address': order.address,
        'lat': coords[1],
        'long': coords[0],
        'items': items
    }


def deliverOrder(req: dict):
    valid, data = getData(req, DeliverOrderForm)
    if not valid:
        return data

    employee, res = _getEmployee(data['uid'])
    if res != None:
        return res
    
    orders = Order.objects.filter(employee=employee, id=uuid.UUID(data['order_id']))
    if len(orders) == 0:
        return {
            'valid': False,
            'message': Messages.ORDER_NOT_FOUND
        }
    orders.update(status='C')
    return {
        'valid': True,
        'message': None
    }



# SETTINGS

def checkPassword(req: dict):
    valid, data = getData(req, PasswordForm)
    if not valid:
        return data

    employee, res = _getEmployee(data['uid'])
    if res != None:
        return res

    if not employee.check_password(data['password']):
        return {
            'valid': False,
            'message': Messages.INCORRECT_PASSWORD,
        }
    
    return {
        'valid': True,
        'message': None
    }


def updatePassword(req: dict):
    valid, data = getData(req, PasswordForm)
    if not valid:
        return data

    employee, res = _getEmployee(data['uid'])
    if res != None:
        return res
    
    employee.password = data['password']
    employee.save()
    return {
        'valid': True,
        'message': None
    }