from django.urls import path

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from warehouse import logic
from misc.logic import queryMedicines

# VIEWS

@api_view(['POST'])
@permission_classes([AllowAny])
def login(req):
    return Response(logic.login(req.data))




@api_view(['GET'])
@permission_classes([AllowAny])
def getEmployees(req):
    return Response(logic.getEmployees(req.GET))


@api_view(['POST'])
@permission_classes([AllowAny])
def addEmployee(req):
    return Response(logic.addEmployee(req.data))


@api_view(['PUT'])
@permission_classes([AllowAny])
def updateEmployee(req):
    return Response(logic.updateEmployee(req.data))


@api_view(['DELETE'])
@permission_classes([AllowAny])
def removeEmployee(req):
    return Response(logic.removeEmployee(req.data))




@api_view(['GET'])
@permission_classes([AllowAny])
def getAttendance(req):
    return Response(logic.getAttendance(req.GET))


@api_view(['POST'])
@permission_classes([AllowAny])
def addEntry(req):
    return Response(logic.addEntry(req.data))




@api_view(['GET'])
@permission_classes([AllowAny])
def getInventory(req):
    return Response(logic.getInventoryItems(req.GET))


@api_view(['GET'])
@permission_classes([AllowAny])
def getMedicines(req):
    return Response(queryMedicines(req.GET))


@api_view(['POST'])
@permission_classes([AllowAny])
def addItem(req):
    return Response(logic.addToInventory(req.data))


@api_view(['PUT'])
@permission_classes([AllowAny])
def updateItem(req):
    return Response(logic.updateItem(req.data))


@api_view(['DELETE'])
@permission_classes([AllowAny])
def removeItem(req):
    return Response(logic.removeItem(req.data))



@api_view(['GET'])
@permission_classes([AllowAny])
def checkPassword(req):
    return Response(logic)

@api_view(['PUT'])
@permission_classes([AllowAny])
def updatePassword(req):
    return Response(logic.updatePassword(req.data))





# URL PATTERNS

urlpatterns = [
    path('login/', login),
    path('add-employee/', addEmployee),
    path('get-employees/', getEmployees),
    path('update-employee/', updateEmployee),
    path('remove-employee/', removeEmployee),
    path('get-attendance/', getAttendance),
    path('add-entry/', addEntry),
    path('get-inventory/', getInventory),
    path('get-medicines/', getMedicines),
    path('add-item/', addItem),
    path('update-item/', updateItem),
    path('remove-item/', removeItem),
    path('check-password/', checkPassword),
    path('update-password/', updatePassword),
]