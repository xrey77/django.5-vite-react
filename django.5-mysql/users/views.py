from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework.parsers import MultiPartParser, JSONParser

from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from users.serializers import UserSerializer
from .models import Users
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

class GetAllUsers(APIView):    
    
    
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')        
        if auth_header:
            try:
                scheme, token = auth_header.split()                
            except ValueError:
                return Response({'message': 'Invalid Authorization'}, status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Unauthorized Access.'}, status=401)

        
        query = Users.objects.all()      
        serializer = UserSerializer(query, many=True)
        if not query.exists():        
            return Response({'message': 'No record(s) found.'}, status.HTTP_400_BAD_REQUEST)
        else:
            serialized_data = serializer.data
            return Response(serialized_data, status.HTTP_200_OK)
    
    
class GetUserId(APIView):    
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')        
        if auth_header:
            try:
                scheme, token = auth_header.split()                
            except ValueError:
                return Response({'message': 'Invalid Authorization'}, status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Unauthorized Access.'}, status=401)
                
        idno = kwargs.get('id') 
        user = Users.objects.filter(id=idno)  
        if user:
            for data in user:
                jsonData = {
                    'id': data.id,
                    'firstname': data.firstname,
                    'lastname': data.lastname,
                    'email': data.email,
                    'mobile': data.mobile,
                    'qrcodeurl': str(data.qrcodeurl),
                    'userpic': str(data.userpic)
                }                
                return Response(jsonData, status.HTTP_200_OK) 

        else:
            return Response({'message': 'User not found.'}, status.HTTP_201_CREATED) 

class DeleteUserId(APIView):    
    def delete(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')        
        if auth_header:
            try:
                scheme, token = auth_header.split()                
            except ValueError:
                return Response({'message': 'Invalid Authorization'}, status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Unauthorized Access.'}, status=401)
                
        idno = kwargs.get('id') 
        user = Users.objects.filter(id=idno)  
        if user:
            User.objects.filter(id=idno).delete()
            return Response({'message': 'User deleted successfully.'}, status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found.'}, status.HTTP_400_BAD_REQUEST) 
            
            
class UpdateProfile(APIView):    
    def patch(self, request, *args, **kwargs):
        idno = request.data.get('id')
        user = Users.objects.get(id=idno)                
        if user:

            partial = request.method == 'PATCH'
            serializer = UserSerializer(user, data=request.data, partial=partial)
            if serializer.is_valid():
                    serializer.save()                                                            
                    return Response({'message': 'Your profile has been successfully updated.'}, status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'User not found.'}, status.HTTP_400_BAD_REQUEST)         
                

class ChangePassword(APIView):    
    def patch(self, request, *args, **kwargs):
        idno = request.data.get('id')
        pwd = request.data.get("password")
                
        validators = [
            MinimumLengthValidator(min_length=8),
            CommonPasswordValidator(),
        ]
        for validator in validators:
            try:
                validator.validate(pwd, user=None)
                
                if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', pwd):
                    raise ValidationError(
                        _("The password must contain at least one special character: " +
                        "!@#$%^&*(),.?\":{}|<>"),
                        code='password_no_symbol',
                    )
                try:    
                    hash = make_password(pwd)        
                    instance = get_object_or_404(Users, id=idno)
                    instance.password = hash
                    instance.save(update_fields=['password'])
                except Exception:
                    print("password not change...")       
                    
                try:
                    userx = Users.objects.filter(id=idno).first()
                    userauth = User.objects.get(username = userx.username)
                    userauth.set_password(pwd)
                    userauth.save()
                    return Response({'message': 'Your password has been successfully updated.'}, status.HTTP_200_OK)                        
                except User.DoesNotExist:
                    print(".")                                                 

            except ValidationError as e:
                return Response({'message': e}, status.HTTP_400_BAD_REQUEST)    



