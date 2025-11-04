from django.urls import path
from .views import RegisterView, LoginView, ProfileView, RegisterDeviceView, DeviceListAdminView, VerifyDeviceView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('devices/register/', RegisterDeviceView.as_view(), name='register-device'),
    path('devices/', DeviceListAdminView.as_view(), name='list-devices'),
    path('devices/verify/<int:device_id>/', VerifyDeviceView.as_view(), name='verify-device'),
]
