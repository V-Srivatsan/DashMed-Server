from django.urls import path, include

urlpatterns = [
    path('api/', include('employee.api.urls'))
]