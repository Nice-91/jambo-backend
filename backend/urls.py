from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def home(request):
    return JsonResponse({"message": "Jambo Backend is running 🚀"})


urlpatterns = [
    path('', home),  # 👈 Add this line — it defines the root route
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/accounts/', include('accounts.urls')),  # accounts endpoints
    path('api/savings/', include('savings.urls')),    # savings endpoints
]
