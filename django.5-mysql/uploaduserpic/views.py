# from rest_framework.exceptions import ValidationError, APIException
from rest_framework.views import APIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from users.serializers import UserSerializer
from users.models import Users
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.deconstruct import deconstructible
from django.shortcuts import get_object_or_404
import os

@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]        
        new_filename = f"{uuid.uuid4().hex}.{ext}"        
        return os.path.join(self.sub_path, new_filename)


class UploadUserpic(APIView):        
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, *args, **kwargs):
      idno = kwargs.get('id')         
      image_file = request.data.get('userpic') 
      if image_file is not None:
        filename = image_file.name             
        base_name, file_extension = os.path.splitext(filename)
        newfilename = "00" + str(idno)
        xfile = newfilename + file_extension
        userpix = 'http://127.0.0.1:8000/media/users/' + xfile
            
        instance = get_object_or_404(Users, id=idno)                            
        partial = request.method == 'PATCH'        
        serializer = UserSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['userpic']  
            extension = uploaded_file.name.split('.')[-1]
            new_name = f"{newfilename}.{extension}"
            uploaded_file.name = new_name                                        
            filepath1 = os.path.join('media/users/', new_name)
            filepath2 = os.path.join('media/users/', newfilename+".jpeg")
            filepath3 = os.path.join('media/users/', newfilename+".png")   
            filepath4 = os.path.join('media/users/', newfilename+".gif")
            filepath5 = os.path.join('media/users/', newfilename+".jpg")            
            if os.path.isfile(filepath1):  
                try:
                    os.remove(filepath1)
                except OSError:
                    print(None)
            if os.path.isfile(filepath2):  
                try:
                 os.remove(filepath2)
                except OSError:
                    print(None)
            if os.path.isfile(filepath3):  
                try:
                  os.remove(filepath3)
                except OSError:
                    print(None)
            if os.path.isfile(filepath4):  
                try:
                  os.remove(filepath4)
                except OSError:
                    print(None)
            if os.path.isfile(filepath5):  
                try:
                  os.remove(filepath5)
                except OSError:
                    print(None)
            try:
                serializer.save()      
            except Exception:
                    print(None)

            try:
                instance.refresh_from_db()
                Users.objects.filter(id=idno).update(userpic=userpix)                
            except Exception:
                print(None)
            return Response({
            'userpic': userpix,
            'message': 'Your profile picture has been changed successfully.' }, status=status.HTTP_200_OK)
