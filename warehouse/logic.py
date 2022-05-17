import uuid
import datetime

from .forms import *
from .models import *
from employee.models import *
from utils import Messages, Patterns, getData, regexValidate


def _getWarehouse(uid: str):
    warehouses = Warehouse.objects.filter(id=uuid.UUID(uid))
    if len(warehouses) > 0:
        return warehouses[0], None

    return None, {
        'valid': False,
        'message': Messages.AUTH_ERROR
    }

def _getEmployee(uid: str, warehouse: Warehouse):
    employees = Employee.objects.filter(id=uuid.UUID(uid), warehouse=warehouse)
    if len(employees) > 0:
        return employees[0]
    return False



def login(req: dict):
    valid, data = getData(req, LoginForm)
    if not valid:
        return data

    warehouses = Warehouse.objects.filter(username=data['username'])
    if len(warehouses) == 0:
        return {
            'valid': False,
            'message': Messages.INVALID_USERNAME,
            'UID': None
        }

    warehouse = warehouses[0]
    if not warehouse.check_password(data['password']):
        return {
            'valid': False,
            'message': Messages.INCORRECT_PASSWORD,
            'UID': None
        }
    
    return {
        'valid': True,
        'message': None,
        'UID': warehouse.id.hex
    }



# Employee Management

def addEmployee(req: dict):
    valid, data = getData(req, AddEmployeeForm)
    if not valid:
        return data

    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res
    
    try:
        employee = Employee(
            warehouse=warehouse, 
            username=data['username'],
            password=data['password'],
            name=data['name'],
            phone=data['phone'],
        )
        employee.save()

    except:
        return {
            'valid': False,
            'message': 'Another employee exists with the same username! Please try another!',
            'uid': None
        }

    return {
        'valid': True,
        'message': None,
        'uid': employee.id.hex
    }


def getEmployees(req: dict):
    valid, data = getData(req, AuthForm)
    if not valid:
        return data

    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res

    return {
        'valid': True,
        'message': None,
        'employees': [{
            'UID': employee.id.hex,
            'name': employee.name,
            'phone': employee.phone
        } for employee in Employee.objects.filter(warehouse=warehouse).order_by('name')]
    }


def updateEmployee(req: dict):
    valid, data = getData(req, UpdateEmployeeForm)
    if not valid:
        return data

    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res

    employee = _getEmployee(data['emp_uid'], warehouse)
    if not employee:
        return {
            'valid': False,
            'message': Messages.EMP_ERROR
        }
    
    employee.name = data['name']
    employee.phone = data['phone']
    employee.save()
    return {
        'valid': True,
        'message': None
    }


def removeEmployee(req: dict):
    valid, data = getData(req, RemoveEmployeeForm)
    if not valid:
        return data
    
    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res
    
    employee = _getEmployee(data['emp_uid'], warehouse)
    if not employee:
        return {
            'valid': False,
            'message': Messages.EMP_ERROR
        }

    employee.delete()
    return {
        'valid': True,
        'message': None
    }



# Attendance Management

def getAttendance(req: dict):
    valid, data = getData(req, EntryForm)
    if not valid:
        return data

    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res

    return {
        'valid': True,
        'message': None,
        'employees': [{
            'UID': entry.employee.id.hex,
            'name': entry.employee.name,
        } for entry in Entry.objects.filter(employee__warehouse=warehouse, date=data['date']).order_by('employee__name')]
    }


def addEntry(req: dict):
    valid, data = getData(req, EntryForm)
    if not valid:
        return data

    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res

    ids = req.get('emp_ids', [])

    if len(ids) == 0:
        return {
            'valid': False,
            'message': Messages.INVALID_DATA
        }

    for id in ids:
        print(id)
        if (regexValidate(id, Patterns.UID)):
            employee = _getEmployee(id, warehouse)
            print(employee)
            if employee:
                Entry(employee=employee, date=data['date']).save()

    return {
        'valid': True,
        'message': None
    }



# Inventory Management

def getInventoryItems(req: dict):
    valid, data = getData(req, AuthForm)
    if not valid:
        return data
    
    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res
    
    return {
        'valid': True,
        'message': None,
        'items': [{
            'uid': item.id.hex,
            'name': item.medicine.name,
            'description': item.medicine.description,
            'composition': item.medicine.composition,
            'expiration': item.medicine.expiration,
            'cost': item.medicine.cost,
            'manufactured': str(item.manufactured),
            'quantity': item.quantity,
        } for item in Item.objects.filter(warehouse=warehouse).order_by('medicine__name')]
    }


def addToInventory(req: dict):
    valid, data = getData(req, AddItemForm)
    if not valid:
        return data

    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res

    medicines = Medicine.objects.filter(id=uuid.UUID(data['med_id']))
    if len(medicines) == 0:
        return {
            'valid': False,
            'message': 'The medicine was not found! Please try again!'
        }

    Item(
        warehouse=warehouse, medicine=medicines[0], 
        manufactured=data['manufactured'],
        quantity=data['quantity']
    ).save()

    return {
        'valid': True,
        'message': None
    }


def updateItem(req: dict):
    valid, data = getData(req, UpdateItemForm)
    if not valid:
        return data
    
    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res
    
    items = Item.objects.filter(id=uuid.UUID(data['item_id']), warehouse=warehouse)
    if len(items) == 0:
        return {
            'valid': False,
            'message': 'This item could not be found on your inventory! Please try again!'
        }

    item = items[0]
    item.quantity = data['quantity']
    item.manufactured = data['manufactured']
    item.save()

    return {
        'valid': True,
        'message': None
    }


def removeItem(req: dict):
    valid, data = getData(req, RemoveItemForm)
    if not valid:
        return data
        
    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res
    
    Item.objects.filter(id=uuid.UUID(data['item_id']), warehouse=warehouse).delete()
    return {
        'valid': True,
        'message': None
    }



# Password

def updatePassword(req: dict):
    valid, data = getData(req, UpdatePasswordForm)
    if not valid:
        return data
        
    warehouse, res = _getWarehouse(data['uid'])
    if res != None:
        return res

    warehouse.password = data['password']
    warehouse.save()
    return {
        'valid': True,
        'message': None
    }