from django.urls import path
from .views import MfaActivate
from .views import MfaVerification

urlpatterns = [
    path('mfa/activate/<int:id>/', MfaActivate.as_view(), name='mfaactivate'),
    path('mfa/verifytotp/<int:id>/', MfaVerification.as_view(), name='mfaverification')
]