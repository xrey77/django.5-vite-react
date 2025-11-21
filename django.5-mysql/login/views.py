from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework import status
from users.models import Users
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError

class UserLogin(APIView):
    
    def post(self, request, *args, **kwargs):
        req = request.data
        usrname = req['username']
        passwd  = req['password']
        try:
          djangoUser = Users.objects.get(username = usrname)           
          if djangoUser: 
                                              
            if check_password(passwd, djangoUser.password): 

                userauth = authenticate(username=usrname, password=passwd)                                                                                                                                
                tokens = get_tokens_for_user(userauth)
                
                return Response({
                    'message': 'Login Successfull.',
                    'id': djangoUser.id,
                    'firstname': djangoUser.firstname,
                    'lastname': djangoUser.lastname,
                    'email': djangoUser.email,
                    'username': djangoUser.username,
                    'roles': djangoUser.roles,
                    'isactivated': djangoUser.isactivated,
                    'isblocked': djangoUser.isblocked,
                    'userpic': str(djangoUser.userpic),
                    'qrcodeurl': str(djangoUser.qrcodeurl),
                    'token': tokens['access']
                    }, status.HTTP_200_OK)
                    
            else:
                return Response({'message': 'Invalid Password, please try again.'}, status.HTTP_404_NOT_FOUND)
            
            
        except Users.DoesNotExist:
            return Response({'message': 'Username not found, please register.'}, status.HTTP_404_NOT_FOUND)

            
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # access_token = refresh.access_token    
    return {
        'refresh': str(refresh),        
        'access': str(refresh.access_token),
    }                    
