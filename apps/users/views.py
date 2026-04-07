from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
import random

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from apps.kyc.models import KYC
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()


# ================= REGISTER =================
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)


# ================= LOGIN =================
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)

        return Response(serializer.errors, status=400)


# ================= USER PROFILE =================
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        user = request.user   # ✅ FIXED

        kyc = KYC.objects.filter(user=user).first()

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "profile_image": user.profile_image.url if user.profile_image else None,
            "kyc_status": kyc.status if kyc else "not_submitted"
        })

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated ✅",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)


# ================= GOOGLE LOGIN =================
class GoogleLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": username}
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        })


# ================= SEND OTP =================
class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        otp = str(random.randint(100000, 999999))

        user.otp = otp
        user.otp_created_at = timezone.now()
        user.is_otp_verified = False
        user.save()

        send_mail(
            "Your OTP Code",
            f"Your OTP is {otp}",
            "your_email@gmail.com",
            [email],
        )

        return Response({"message": "OTP sent"})


# ================= VERIFY OTP =================
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.otp_created_at and timezone.now() > user.otp_created_at + timedelta(minutes=5):
            return Response({"error": "OTP expired"}, status=400)

        if user.otp != otp:
            return Response({"error": "Invalid OTP"}, status=400)

        user.is_otp_verified = True
        user.save()

        return Response({"message": "OTP verified"})


# ================= RESET PASSWORD =================
class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not user.is_otp_verified:
            return Response({"error": "OTP not verified"}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful"})


# ================= CHANGE PASSWORD =================
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password incorrect ❌"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully 🔥"})


# ================= ADMIN USERS =================
class AdminUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"error": "Not allowed"}, status=403)

        users = User.objects.all()

        data = [
            {
                "id": u.id,
                "email": u.email,
                "role": u.role,
                "is_blocked": u.is_blocked,
            }
            for u in users
        ]

        return Response(data)


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        if request.user.role != "admin":
            return Response({"error": "Not allowed"}, status=403)

        user = User.objects.get(id=id)
        user.is_blocked = True
        user.save()

        return Response({"message": "User blocked"})


class UnblockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        if request.user.role != "admin":
            return Response({"error": "Not allowed"}, status=403)

        user = User.objects.get(id=id)
        user.is_blocked = False
        user.save()

        return Response({"message": "User unblocked"})