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
          djangoUser = User.objects.get(username = usrname)           
          if djangoUser: 
            userauth = authenticate(username=usrname, password=passwd)
            if userauth is not None:
            
                xuser = Users.objects.filter(username=usrname).first()
                if xuser:
                    
                    # for data in user:
                    if check_password(passwd, xuser.password): 

                                                                                                                                    
                        tokens = get_tokens_for_user(userauth)
                        
                        return Response({
                            'message': 'Login Successfull.',
                            'id': xuser.id,
                            'firstname': xuser.firstname,
                            'lastname': xuser.lastname,
                            'email': xuser.email,
                            'username': xuser.username,
                            'roles': xuser.roles,
                            'isactivated': xuser.isactivated,
                            'isblocked': xuser.isblocked,
                            'userpic': str(xuser.userpic),
                            'qrcodeurl': str(xuser.qrcodeurl),
                            'token': tokens['access']
                            }, status.HTTP_200_OK)
                            
                    else:
                        return Response({'message': 'Invalid Password.'}, status.HTTP_404_NOT_FOUND)
                    
                else:
                    return Response({'message': 'Username not found'}, status.HTTP_404_NOT_FOUND)            
                
            else:
                return Response({'message': 'Invalid Credentials.'}, status.HTTP_406_NOT_ACCEPTABLE) 
                                    
            
        except User.DoesNotExist:
            return Response({'message': 'Username not found.'}, status.HTTP_404_NOT_FOUND)

                    # return Response({'message': 'Invalid Credentials.' }, status.HTTP_400_BAD_REQUEST) 
        # except ObjectDoesNotExist:            
        #             return Response({'message': 'Invalid Credentials.'}, status.HTTP_404_NOT_FOUND) 
        # except FileNotFoundError:            
        #             return Response({'message': 'Invalid Credentials.'}, status.HTTP_404_NOT_FOUND) 
            
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # access_token = refresh.access_token    
    return {
        'refresh': str(refresh),        
        'access': str(refresh.access_token),
    }                    
