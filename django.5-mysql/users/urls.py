from django.urls import path
from .views import GetAllUsers
from .views import GetUserId
from .views import DeleteUserId
from .views import UpdateProfile
from .views import ChangePassword

urlpatterns = [
    path('getuserid/<int:id>/', GetUserId.as_view(), name='getuserid'),
    path('getallusers/', GetAllUsers.as_view(), name='getallusers'),    
    path('deleteuser/<int:id>/', DeleteUserId.as_view(), name='deleteuser'),
    path('updateprofile/', UpdateProfile.as_view(), name='updateprofile'),
    path('changepassword/', ChangePassword.as_view(), name='changepassword'),
]