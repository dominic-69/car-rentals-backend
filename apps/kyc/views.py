from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import KYC
from .serializers import KYCSerializer
from django.core.mail import send_mail
import cloudinary.uploader


# ==============================
# 🔐 CUSTOM ADMIN PERMISSION
# ==============================
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


 
class SubmitKYCView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        kyc = KYC.objects.filter(user=request.user).first()

        if kyc and kyc.status == "approved":
            return Response({"error": "KYC already approved"}, status=400)

        try:
            license_file = request.FILES.get("license_image")
            selfie_file = request.FILES.get("selfie_image")

            license_upload = cloudinary.uploader.upload(
                license_file, folder="kyc/licenses"
            )

            selfie_upload = cloudinary.uploader.upload(
                selfie_file, folder="kyc/selfies"
            )

            if kyc:
                kyc.full_name = request.data.get("full_name")
                kyc.license_number = request.data.get("license_number")
                kyc.license_image = license_upload["secure_url"]
                kyc.selfie_image = selfie_upload["secure_url"]
                kyc.status = "pending"
                kyc.rejection_reason = ""
                kyc.save()
            else:
                KYC.objects.create(
                    user=request.user,
                    full_name=request.data.get("full_name"),
                    license_number=request.data.get("license_number"),
                    license_image=license_upload["secure_url"],
                    selfie_image=selfie_upload["secure_url"],
                )

            return Response({"message": "KYC submitted successfully ✅"})

        except Exception as e:
            return Response({"error": str(e)}, status=400)

 
class MyKYCView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            kyc = KYC.objects.get(user=request.user)
            serializer = KYCSerializer(kyc)
            return Response(serializer.data)
        except KYC.DoesNotExist:
            return Response({"message": "No KYC found"})

 
class AdminKYCListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        kyc = KYC.objects.all()
        serializer = KYCSerializer(kyc, many=True)
        return Response(serializer.data)

 
class ApproveKYCView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, id):
        try:
            kyc = KYC.objects.get(id=id)
        except KYC.DoesNotExist:
            return Response({"error": "KYC not found"}, status=404)

        kyc.status = "approved"
        kyc.save()

        send_mail(
            "KYC Approved ✅",
            "Your KYC has been successfully approved.",
            "dominicproject96@gmail.com",
            [kyc.user.email],
            fail_silently=True,
        )

        return Response({"message": "KYC approved"})


 
class RejectKYCView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, id):
        try:
            kyc = KYC.objects.get(id=id)
        except KYC.DoesNotExist:
            return Response({"error": "KYC not found"}, status=404)

        reason = request.data.get("reason", "Not specified")

        kyc.status = "rejected"
        kyc.rejection_reason = reason
        kyc.save()

        send_mail(
            "KYC Rejected ❌",
            f"Your KYC was rejected.\nReason: {reason}",
            "dominicproject96@gmail.com",
            [kyc.user.email],
            fail_silently=True,
        )

        return Response({"message": "KYC rejected"})