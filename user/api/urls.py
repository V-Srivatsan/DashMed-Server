from django.urls import path

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from user import logic
from misc.logic import queryMedicines

# VIEWS

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(req):
    return Response(logic.signupUser(req.data))


@api_view(['POST'])
@permission_classes([AllowAny])
def login(req):
    return Response(logic.loginUser(req.data))


@api_view(['POST'])
@permission_classes([AllowAny])
def order(req):
    return Response(logic.order(req.data))


@api_view(['PUT'])
@permission_classes([AllowAny])
def updateProfile(req):
    return Response(logic.updateUser(req.data))


@api_view(['DELETE'])
@permission_classes([AllowAny])
def deleteProfile(req):
    return Response(logic.deleteUser(req.data))
    

@api_view(['GET'])
@permission_classes([AllowAny])
def getOrderCounts(req):
    return Response(logic.getOrderCount(req.GET))


@api_view(['GET'])
@permission_classes([AllowAny])
def getOrders(req):
    return Response(logic.getOrders(req.GET))

@api_view(['GET'])
@permission_classes([AllowAny])
def getOrder(req):
    return Response(logic.getOrder(req.GET))

@api_view(['GET'])
@permission_classes([AllowAny])
def getMedicines(req):
    return Response(queryMedicines(req.GET))


@api_view(['GET'])
@permission_classes([AllowAny])
def checkPassword(req):
    return Response(logic.checkPassword(req.GET))





# URL_PATTERNS

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('order/', order),
    path('update/', updateProfile),
    path('get-order-count/', getOrderCounts),
    path('get-orders/', getOrders),
    path('get-order/', getOrder),
    path('get-medicines/', getMedicines),
    path('check-password/', checkPassword),
]