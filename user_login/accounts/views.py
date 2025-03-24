from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi  


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="User registration",
        request_body=RegisterSerializer,
        responses={201: "User created successfully", 400: "Bad request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="User login",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "access": "your_access_token",
                        "refresh": "your_refresh_token"
                    }
                }
            ),
            401: "Invalid credentials",
            400: "Bad request"
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                
                # Bu sətri sildim: user.delete()

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="User logout",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            },
            required=['refresh_token']
        ),
        responses={
            200: "Logout successful",
            400: "Invalid token"
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            
            # Token blacklist etmədən əvvəl istifadəçini əldə edin
            user_id = token.payload.get('user_id')
            user = User.objects.get(id=user_id)
            
            # Tokeni blacklist edin
            token.blacklist()
            
            # İstifadəçini sistemdən çıxarın
            logout(request)
            
            # İstifadəçini silin
            user.delete()

            return Response({"msg": "Logout successful and user deleted"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"msg": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)