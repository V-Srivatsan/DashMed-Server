from django.contrib.gis.geos import Point
import uuid

from user.models import User
from warehouse.models import Warehouse
from .models import Admin
from misc.models import *

from .forms import *
import utils
from utils import Messages, getData


ADMIN_NOT_FOUND = {
    'valid': False,
    'message': Messages.AUTH_ERROR
}


def _isAdmin(uid: str) -> bool:
    admin = Admin.objects.filter(id=uuid.UUID(uid))
    if len(admin) == 0:
        return False    
    return True



def login(req: dict):
    valid, data = getData(req, LoginForm)
    if not valid:
        return data
    
    admins = Admin.objects.filter(username=data['username'])
    if len(admins) == 0:
        return {
            'valid': False,
            'message': Messages.INVALID_USERNAME
        }
    
    admin: Admin = admins[0]
    if not admin.check_password(data['password']):
        return {
            'valid': False,
            'message': Messages.INCORRECT_PASSWORD
        }

    return {
        'valid': True,
        'UID': admin.id.hex
    }




def getUserByUsername(req: dict):
    valid, data = getData(req, GetUserForm)
    if not valid:
        return data

    if not _isAdmin(data['uid']):
        return ADMIN_NOT_FOUND

    users = User.objects.filter(username=data['username'])
    if len(users) == 0:
        return { 'valid': True }

    user: User = users[0]
    return {
        'valid': True,
        'user': {
            'uid': user.id.hex,
            'name': user.name,
            'phone': user.phone,
            'email': user.email,
        }
    }


def updateUser(req: dict):
    valid, data = getData(req, UpdateUserForm)
    if not valid:
        return data

    if not _isAdmin(data['uid']):
        return ADMIN_NOT_FOUND

    users = User.objects.filter(id=uuid.UUID(data['user_id']))
    if len(users) == 0:
        return {
            'valid': False,
            'message': Messages.USER_ERROR
        }
    
    user = users[0]
    user.password = data['password']
    user.save()

    return { 'valid': True }




def getWarehouses(req: dict):
    valid, data = getData(req, GetWarehousesForm)
    if not valid:
        return data
    
    if not _isAdmin(data['admin']):
        return ADMIN_NOT_FOUND
    
    return {
        'valid': True,
        'warehouses': [{
            'uid': warehouse.id.hex,
            'name': warehouse.name,
            'address': warehouse.address,
            'lat': warehouse.coords.tuple[1],
            'long': warehouse.coords.tuple[0],
        } for warehouse in Warehouse.objects.filter(name__search=data['name'])]
    }


def setupWarehouse(req: dict):
    valid, data = getData(req, AddWarehouseForm)
    if not valid:
        return data

    if not _isAdmin(data['uid']):
        return ADMIN_NOT_FOUND

    id = utils.addWarehouse(
        data['username'], data['password'], 
        data['name'], data['address'], (data['lat'], data['long'])
    )

    if not id:
        return {
            'valid': False,
            'message': Messages.INVALID_USERNAME
        }
    
    return { 
        'valid': True,
        'UID': id
    }


def updateWarehouse(req: dict):
    valid, data = getData(req, UpdateWarehouseForm)
    if not valid:
        return data
    
    if not _isAdmin(data['uid']):
        return ADMIN_NOT_FOUND
    
    Warehouse.objects.filter(id=uuid.UUID(data['warehouse_id'])).update(
        name=data['name'],
        address=data['address'],
        coords=Point(data['long'], data['lat'])
    )
    return { 'valid': True }


def removeWarehouse(req: dict):
    valid, data = getData(req, RemoveWarehouseForm)
    if not valid:
        return data
    
    if not _isAdmin(data['uid']):
        return ADMIN_NOT_FOUND
    
    Warehouse.objects.filter(id=uuid.UUID(data['warehouse_id'])).delete()
    return { 'valid': True }




def getMedicines(req: dict):
    valid, data = getData(req, GetMedicinesForm)
    if not valid:
        return data
    
    if not _isAdmin(data['uid']):
        return ADMIN_NOT_FOUND
    
    return {
        'valid': True,
        'medicines': [{
            'uid': medicine.id.hex,
            'name': medicine.name,
            'description': medicine.description,
            'composition': medicine.composition,
            'expiration': medicine.expiration,
            'cost': medicine.cost,
        } for medicine in Medicine.objects.all()]
    }


def addMedicine(req: dict):
    valid, data = getData(req, AddMedicineForm)
    if not valid:
        return data
    
    if not _isAdmin(data['uid']):
        return ADMIN_NOT_FOUND

    composition = req.get('composition', [])
    if len(composition) == 0:
        return {
            'valid': False,
            'message': Messages.INVALID_DATA
        }

    id = utils.addMedicine(
        data['name'], data['description'], composition,
        data['expiration'], data['cost']
    )
    return {
        'valid': True,
        'UID': id
    }


def updateMedicine(req: dict):
    valid, data = getData(req, UpdateMedicineForm)
    if not valid:
        return data
    
    if not _isAdmin(data['uid']):
        return ADMIN_NOT_FOUND

    composition = req.get('composition', [])
    if len(composition) == 0:
        return {
            'valid': False,
            'message': Messages.INVALID_DATA
        }

    Medicine.objects.filter(id=uuid.UUID(data['med_id'])).update(
        name=data['name'],
        description=data['description'],
        composition=composition,
        expiration=data['expiration'],
        cost=data['cost'],
        searchable=data['searchable']
    )

    return { 'valid': True }




def checkPassword(req: dict):
    valid, data = getData(req, PasswordForm)
    if not valid:
        return data
    
    admins = Admin.objects.filter(id=uuid.UUID(data['uid']))
    if len(admins) == 0:
        return ADMIN_NOT_FOUND
    
    if not admins[0].check_password(data['password']):
        return {
            'valid': False,
            'message': Messages.INCORRECT_PASSWORD
        }

    return { 'valid': True }


def updatePassword(req: dict):
    valid, data = getData(req, PasswordForm)
    if not valid:
        return data

    Admin.objects.filter(id=uuid.UUID(data['uid'])).update(password=data['password'])
    return { 'valid': True }