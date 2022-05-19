from django.urls import path

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from dba import logic



# VIEWS

@api_view(['POST'])
@permission_classes([AllowAny])
def login(req):
    return Response(logic.login(req.data))

@api_view(['GET'])
@permission_classes([AllowAny])
def getUser(req):
    return Response(logic.getUserByUsername(req.GET))

@api_view(['PUT'])
@permission_classes([AllowAny])
def updateUser(req):
    return Response(logic.updateUser(req.data))

@api_view(['GET'])
@permission_classes([AllowAny])
def getWarehouse(req):
    return Response(logic.getWarehouses(req.GET))

@api_view(['POST'])
@permission_classes([AllowAny])
def addWarehouse(req):
    return Response(logic.setupWarehouse(req.data))

@api_view(['PUT'])
@permission_classes([AllowAny])
def updateWarehouse(req):
    return Response(logic.updateWarehouse(req.data))

@api_view(['DELETE'])
@permission_classes([AllowAny])
def removeWarehouse(req):
    return Response(logic.removeWarehouse(req.data))

@api_view(['GET'])
@permission_classes([AllowAny])
def getMedicines(req):
    return Response(logic.getMedicines(req.GET))

@api_view(['POST'])
@permission_classes([AllowAny])
def addMedicine(req):
    return Response(logic.addMedicine(req.data))

@api_view(['PUT'])
@permission_classes([AllowAny])
def updateMedicine(req):
    return Response(logic.updateMedicine(req.data))

@api_view(['GET'])
@permission_classes([AllowAny])
def checkPassword(req):
    return Response(logic.checkPassword(req.GET))

@api_view(['PUT'])
@permission_classes([AllowAny])
def updatePassword(req):
    return Response(logic.updatePassword(req.data))






# URLPATTERNS

urlpatterns = [
    path('login/', login),
    path('get-user/', getUser),
    path('update-user/', updateUser),
    path('get-warehouse/', getWarehouse),
    path('add-warehouse/', addWarehouse),
    path('update-warehouse/', updateWarehouse),
    path('remove-warehouse/', removeWarehouse),
    path('get-meds/', getMedicines),
    path('add-med/', addMedicine),
    path('update-med/', updateMedicine),
    path('check-password/', checkPassword),
    path('update-password/', updatePassword)
]