from django.urls import path
from .views import UploadUserpic

urlpatterns = [
    path('uploadpicture/<int:id>/', UploadUserpic.as_view(), name='uploadpicture')
]