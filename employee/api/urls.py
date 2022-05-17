from django.urls import path

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from employee import logic


# VIEWS

@api_view(['POST'])
@permission_classes([AllowAny])
def login(req):
    return Response(logic.login(req.data))

@api_view(['GET'])
@permission_classes([AllowAny])
def getPending(req):
    return Response(logic.getPendingOrders(req.GET))

@api_view(['GET'])
@permission_classes([AllowAny])
def getOrder(req):
    return Response(logic.getOrder(req.GET))

@api_view(['PUT'])
@permission_classes([AllowAny])
def deliverOrder(req):
    return Response(logic.deliverOrder(req.data))

@api_view(['GET'])
@permission_classes([AllowAny])
def checkPassword(req):
    return Response(logic.checkPassword(req.GET))

@api_view(['PUT'])
@permission_classes([AllowAny])
def updatePassword(req):
    return Response(logic.updatePassword(req.data))





# URL PATTERNS

urlpatterns = [
    path('login/', login),
    path('get-pending/', getPending),
    path('get-order/', getOrder),
    path('deliver-order/', deliverOrder),
    path('check-password/', checkPassword),
    path('change-password/', updatePassword),
]