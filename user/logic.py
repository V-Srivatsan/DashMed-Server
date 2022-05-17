from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

import uuid
import datetime
import math

from utils import Messages, getData
from .forms import *
from misc.models import Medicine
from .models import *
from warehouse.models import *



def _getUser(uid: str) -> User:
    users = User.objects.filter(id=uuid.UUID(uid))
    if len(users) > 0:
        return users[0]
    return False



# AUTH

def signupUser(req: dict):
    valid, data = getData(req, SignupForm)
    if not valid:
        return data

    if len(User.objects.filter(username=data['username'])) != 0:
        return {
            'valid': False,
            'message': Messages.USERNAME_TAKEN,
        }

    user = User(**data)
    user.save()
    return {
        'valid': True,
        'message': None,
        'UID': user.id.hex
    }


def loginUser(req: dict):
    valid, data = getData(req, LoginForm)
    if not valid:
        return data

    users = User.objects.filter(username=data['username'])
    if len(users) == 0:
        return {
            'valid': False,
            'message': Messages.INVALID_USERNAME
        }

    user = users[0]
    if not user.check_password(data['password']):
        return {
            'valid': False,
            'message': Messages.INCORRECT_PASSWORD
        }

    return {
        'valid': True,
        'message': None,
        'UID': user.id.hex,
    }


def checkPassword(req: dict):
    valid, data = getData(req, CheckPasswordForm)
    if not valid:
        return data

    user = _getUser(data['uid'])
    if not user:
        return {
            'valid': False,
            'message': Messages.AUTH_ERROR
        }

    if not user.check_password(data['password']):
        return {
            'valid': False,
            'message': Messages.INCORRECT_PASSWORD
        }

    return {
        'valid': True,
        'message': None,
        'name': user.name,
        'email': user.email,
        'phone': user.phone
    }



# PROFILE

def updateUser(req: dict):
    valid, data = getData(req, UpdateUserForm)
    if not valid:
        return data

    user = _getUser(data['uid'])
    if not user:
        return {
            'valid': False,
            'message': Messages.AUTH_ERROR
        }

    user.name = data['name']
    user.phone = data['phone']
    user.email = data['email']
    user.password = data['password']
    user.save()

    return {
        'valid': True,
        'message': None
    }


def deleteUser(req: dict):
    valid, data = getData(req, AuthForm)
    if not valid:
        return data

    user = _getUser(data['uid'])
    if not user:
        return {
            'valid': False,
            'message': Messages.AUTH_ERROR
        }

    user.delete()
    return {
        'valid': True,
        'message': None
    }



# ORDERS

def getOrderCount(req: dict):
    valid, data = getData(req, AuthForm)
    if not valid:
        return data

    user = _getUser(data['uid'])
    if not user:
        return {
            'valid': False,
            'message': Messages.AUTH_ERROR,
            'counts': None
        }

    counts = [0, 0, 0, 0, 0]
    orders = Order.objects.filter(user=user).order_by('-order_date')
    for i in range(min(len(orders), 5)):
        value = 0
        for item in orders[i].items:
            value += int(item['quantity'])
        counts[4 - i] = value

    return {
        'valid': True,
        'message': None,
        'counts': counts
    }


def getOrders(req: dict):
    valid, data = getData(req, AuthForm)
    if not valid:
        return data

    user = _getUser(data['uid'])
    if not user:
        return {
            'valid': False,
            'message': Messages.AUTH_ERROR,
        }

    dataset = Order.objects.filter(user=user).order_by('-order_date')
    orders = []

    for i in range(len(dataset)):
        order = dataset[i]
        orders.append({
            'uid': order.id.hex,
            'date': str(order.order_date),
            'status': order.status == 'C',
            'length': len(order.items)
        })

    return {
        'valid': True,
        'message': None,
        'orders': orders
    }


def getOrder(req: dict):
    valid, data = getData(req, GetOrderItemsForm)
    if not valid:
        return data

    orders = Order.objects.filter(
        id=uuid.UUID(data['order_id']),
        user__id=uuid.UUID(data['uid'])
        )

    if len(orders) == 0:
        return {
            'valid': False,
            'message': Messages.ORDER_NOT_FOUND
        }

    items, order = [], orders[0]
    for item in order.items:
        medicine = Medicine.objects.get(id=uuid.UUID(item['med_id']))
        items.append({
            'name': medicine.name,
            'description': medicine.description,
            'composition': medicine.composition,
            'expiration': medicine.expiration,
            'cost': medicine.cost,
            'quantity': item['quantity']
        })
    
    coords = order.coords.tuple
    return { 
        'valid': True, 
        'message': None,
        'items': items,
        'address': order.address,
        'lat': coords[1],
        'long': coords[0],
        'employee': {
            'name': order.employee_name,
            'phone': order.employee_phone,
        }
    }


def order(req: dict):
    valid, data = getData(req, PlaceOrderForm)
    if not valid:
        return data
    
    user = _getUser(data['uid'])
    point = Point(data['long'], data['lat'])
    if not user:
        return {
            'valid': False,
            'message': Messages.AUTH_ERROR,
        }

    items, medicines, quantities = [], [], []
    meds = req.get('meds', [])

    for item in meds:
        item_valid, med = getData(item, MedForm)
        if item_valid:
            medicine = Medicine.objects.get(id=uuid.UUID(med['uid']), searchable=True)
            items.append({
                'med_id': med['uid'],
                'quantity': med['quantity']
            })
            medicines.append(medicine)
            quantities.append(med['quantity'])

    if len(items) == 0:
        return {
            'valid': False,
            'message': Messages.INVALID_DATA
        }

    warehouses = []
    for warehouse in Warehouse.objects.filter(coords__distance_lt=(point, Distance(km=5))):
        valid = True
        for i in range(len(medicines)):
            if len(Item.objects.filter(warehouse=warehouse, medicine=medicines[i], quantity__gt=quantities[i])) == 0:
                valid = False
                break
        if valid: warehouses.append(warehouse)

    if len(warehouses) == 0:
        return {
            'valid': False,
            'message': 'No nearby warehouses were found!'
        }

    employees = Employee.objects.filter(entry__date=datetime.datetime.today().date(), warehouse__in=warehouses)
    employee, min_pending = None, math.inf
    for emp in employees:
        pending = Order.objects.filter(employee=emp, status='P').count()
        if (pending == 0):
            employee = emp
            break
        elif (pending < min_pending):
            min_pending = pending
            employee = emp

    if employee == None:
        return {
            'valid': False,
            'message': 'No employees were found nearby! Please try again after some time!'
        }

    for i in range(len(medicines)):
        medicine = medicines[i]
        item = Item.objects.filter(warehouse=employee.warehouse, medicine=medicine).order_by('-manufactured')[0]
        item.quantity -= quantities[i]
        item.save()

    Order(
        employee=employee,
        user=user,
        items=items,
        address=data['address'],
        coords=point
    ).save()

    return {
        'valid': True,
        'message': None
    }