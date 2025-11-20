from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from users.models import Users
from django.contrib.auth.models import User


class UserRegistration(APIView):
    
    def post(self, request, *args, **kwargs):
        req = request.data
        emailAdd = req['email']
        userName = req['username']
        passWord = req['password']
        
        validators = [
            MinimumLengthValidator(min_length=8),
            CommonPasswordValidator(),
        ]
        for validator in validators:
            try:
                validator.validate(passWord, user=None)
                
                if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', passWord):
                    raise ValidationError(
                        _("The password must contain at least one special character: " +
                        "!@#$%^&*(),.?\":{}|<>"),
                        code='password_no_symbol',
                    )
                    
                userEmail = Users.objects.filter(email__exact = emailAdd).first()        
                if userEmail:
                    return Response({'message': 'Email Address is already taken.'}, status.HTTP_200_OK)          

                usrName = Users.objects.filter(username__exact = userName).first()        
                if usrName:
                    return Response({'message': 'Username is already taken.'}, status.HTTP_200_OK)          
                                    
                hash = make_password(req['password'])        
                jsonData = {
                    'firstname': req['firstname'],
                    'lastname': req['lastname'],
                    'email': req['email'],
                    'mobile': req['mobile'],
                    'roles': 'ROLE_USER',
                    'username': req['username'],
                    'password': hash,
                    'isactivated': True,
                    'isblocked': False
                }
                
                serializer = UserSerializer(data=jsonData)
                if serializer.is_valid():
                    xuser = serializer.save()
                    xuser.userpic = "http://127.0.0.1:8000/media/images/pix.png"
                    xuser.save()
                    
                    userauth = User.objects.create_superuser(username=userName, email=emailAdd)
                    userauth.set_password(passWord)
                    userx = userauth.save()
                                
                    return Response({'message': 'You have registered succesfully.'}, status.HTTP_201_CREATED)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)                    
                                    
            except ValidationError as e:
                return Response({'message': e.messages}, status.HTTP_400_BAD_REQUEST)    
        
        

def validate_password(password, user=None):
    validators = [
        MinimumLengthValidator(min_length=9), # Example of custom configuration
        CommonPasswordValidator(),
    ]
    for validator in validators:
        try:
            validator.validate(password, user=user)
        except ValidationError as e:
            # Handle error
            print(f"Password error: {e.messages}")
            return False # Invalid
    return True # Valid
