from rest_framework.views import APIView
from django.shortcuts import render
# from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from users.models import Users
import pyotp
import qrcode
import base64
from io import BytesIO
from PIL import Image

class MfaActivate(APIView):
    
    def patch(self, request, *args, **kwargs):
        isEnabled = request.data.get('TwoFactorEnabled')
        idno = kwargs.get('id') 
        if isEnabled:
            user = Users.objects.filter(id=idno).first()
            if user:
                
                secret_key = pyotp.random_base32()    
                totp = pyotp.TOTP(secret_key)        
                qrcodeuri = totp.provisioning_uri(name=user.email, issuer_name='SUPERCARS INC.')
                qrcode_base64 = generate_qr_code_base64(qrcodeuri)                
                # print(qrcode_base64)
                # partial = request.method == 'PATCH'
                # jsonData = {
                #     'secret': secret_key,
                #     'qrcodeurl': qrcode_base64
                # }
                
                Users.objects.filter(id=idno).update(secret=secret_key, qrcodeurl=qrcode_base64)                

                # serializer = UserSerializer(user, data=jsonData, partial=partial)
                # if serializer.is_valid():
                #     qrcodeb64 = serializer.save()                    
                #     qrcodeb64.qrcodeurl = qrcode_base64
                #     qrcodeb64.save()
                return Response({
                    'qrcodeurl': qrcode_base64,
                    'message': 'Multi-Factor Authenticator is enabled.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)           
        else:            
            user = Users.objects.get(id=idno)                
            if user:
                partial = request.method == 'PATCH'
                user.secret = None
                user.qrcodeurl  = None
                user.save()
                return Response({'message': 'Multi-Factor Authenticator is disabled.'}, status=status.HTTP_201_CREATED)
        
class MfaVerification(APIView):    
    def patch(self, request, *args, **kwargs):
        idno = kwargs.get('id') 
        otp = request.data.get('otp')        
        user = Users.objects.get(id=idno)
        secret = user.secret
        totp = pyotp.TOTP(secret)                
        isValid = totp.verify(otp)        
        if isValid:
            return Response({
                'username': user.username,
                'message': 'Successfull OTP code verification.'}, status=status.HTTP_200_OK)
        else:                
            return Response({'message': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
def generate_qr_code_base64(data):
    # Generate the QR code image using the qrcode library
    qr_img = qrcode.make(data)

    # Save the image to a BytesIO buffer
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Encode the image bytes to base64
    encoded_img = base64.b64encode(buffer.read()).decode()
    
    # Format for direct display in an HTML img tag or a frontend app
    qr_code_data = f'data:image/png;base64,{encoded_img}'
    
    return qr_code_data