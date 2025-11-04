from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Device
from .serializers import UserSerializer, DeviceSerializer


# -----------------------------
# Register
# -----------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not email or not username or not password:
            return Response({"error": "Email, username, and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


# -----------------------------
# Login (with device verification)
# -----------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        device_id = request.data.get('device_id')

        if not email or not password or not device_id:
            return Response(
                {"error": "Email, password, and device_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate using EmailBackend (make sure AUTHENTICATION_BACKENDS includes your backend)
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check device
        try:
            device = Device.objects.get(user=user, device_id=device_id)
            if not device.is_verified:
                return Response({"error": "Device not verified"}, status=status.HTTP_403_FORBIDDEN)
        except Device.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)


# -----------------------------
# Profile
# -----------------------------
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# -----------------------------
# Device Management
# -----------------------------
class RegisterDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        device_id = request.data.get('device_id')
        if not device_id:
            return Response({"error": "Device ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        device, created = Device.objects.get_or_create(user=request.user, device_id=device_id)
        message = "Device registered. Waiting for admin verification." if created else "Device already registered."
        return Response({"message": message, "device": DeviceSerializer(device).data})


class DeviceListAdminView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAdminUser]
    queryset = Device.objects.all()


class VerifyDeviceView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        device.is_verified = True
        device.save()
        return Response({"message": "Device verified successfully"})
