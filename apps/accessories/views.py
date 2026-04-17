from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Accessory, AccessoryImage
from .serializers import AccessorySerializer
from .permissions import IsSeller

import cloudinary.uploader


# =========================
# 🔥 CREATE ACCESSORY
# =========================
class CreateAccessoryView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request):
        data = request.data

        accessory = Accessory.objects.create(
            seller=request.user,
            name=data.get("name"),
            brand=data.get("brand"),
            price=data.get("price"),
            stock=data.get("stock"),
            description=data.get("description"),
            category=data.get("category"),
        )

        # 🔥 IMAGES
        images = request.FILES.getlist("images")

        if len(images) > 5:
            return Response({"error": "Max 5 images allowed ❌"}, status=400)

        for img in images:
            upload = cloudinary.uploader.upload(img)
            AccessoryImage.objects.create(
                accessory=accessory,
                image=upload["secure_url"]
            )

        return Response({"message": "Accessory added ✅"})


# =========================
# 🔥 MY ACCESSORIES (SELLER)
# =========================
class MyAccessoriesView(generics.ListAPIView):
    serializer_class = AccessorySerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        return Accessory.objects.filter(seller=self.request.user)


# =========================
# 🔥 ALL ACCESSORIES (USER)
# =========================
class AccessoryListView(generics.ListAPIView):
    serializer_class = AccessorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.role == "admin":
            return Accessory.objects.all()

        return Accessory.objects.filter(is_approved=True)
# =========================
# 🔥 DETAIL
# =========================
class AccessoryDetailView(generics.RetrieveAPIView):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]


# =========================
# 🔥 UPDATE ACCESSORY
# =========================
class AccessoryUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def put(self, request, id):
        try:
            accessory = Accessory.objects.get(id=id)
        except Accessory.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        # 🔐 OWNER CHECK
        if accessory.seller != request.user:
            return Response({"error": "Unauthorized"}, status=403)

        data = request.data

        accessory.name = data.get("name", accessory.name)
        accessory.brand = data.get("brand", accessory.brand)
        accessory.price = data.get("price", accessory.price)
        accessory.stock = data.get("stock", accessory.stock)
        accessory.description = data.get("description", accessory.description)
        accessory.category = data.get("category", accessory.category)

        # 🔥 REQUIRE RE-APPROVAL AFTER EDIT
        accessory.is_approved = False

        accessory.save()

        # 🔥 IMAGES
        images = request.FILES.getlist("images")

        if images:
            if len(images) > 5:
                return Response({"error": "Max 5 images allowed ❌"}, status=400)

            AccessoryImage.objects.filter(accessory=accessory).delete()

            for img in images:
                upload = cloudinary.uploader.upload(img)
                AccessoryImage.objects.create(
                    accessory=accessory,
                    image=upload["secure_url"]
                )

        return Response({"message": "Updated ✅"})


# =========================
# 🔥 DELETE ACCESSORY
# =========================
class AccessoryDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def delete(self, request, id):
        try:
            accessory = Accessory.objects.get(id=id)
        except Accessory.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        # 🔐 OWNER CHECK
        if accessory.seller != request.user:
            return Response({"error": "Unauthorized"}, status=403)

        accessory.delete()
        return Response({"message": "Deleted ✅"})


# =========================
# 🔥 ADMIN APPROVE
# =========================
class ApproveAccessoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        if request.user.role != "admin":
            return Response({"error": "Unauthorized ❌"}, status=403)

        try:
            accessory = Accessory.objects.get(id=id)
        except Accessory.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        accessory.is_approved = True
        accessory.save()

        return Response({"message": "Approved ✅"})