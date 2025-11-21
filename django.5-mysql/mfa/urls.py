from django.urls import path
from .views import MfaActivate
from .views import MfaVerification
from .views import MfaQrcode

urlpatterns = [
    path('mfa/activate/<int:id>/', MfaActivate.as_view(), name='mfaactivate'),
    path('mfa/verifytotp/<int:id>/', MfaVerification.as_view(), name='mfaverification'),
    path('mfa/getqrcode/<int:id>/', MfaQrcode.as_view(), name='getqrcode'),
]