from django.urls import path
from .views import UserLogin

urlpatterns = [
    path('signin/', UserLogin.as_view(), name="signin"),
]