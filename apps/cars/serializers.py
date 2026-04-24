from rest_framework import serializers
from .models import Car, CarImage


# =========================
# 🖼 CAR IMAGE SERIALIZER
# =========================
class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ["id", "image"]


# =========================
# 🚗 CAR SERIALIZER
# =========================
class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            "id",
            "title",
            "brand",
            "price",
            "location",
            "description",
            "registration_number",
            "fuel_type",
            "transmission",
            "seats",
            "latitude",
            "longitude",
            "images",
            "seller",
        ]

    # =========================
    # 👤 SAFE SELLER METHOD
    # =========================
    def get_seller(self, obj):
        # 🔥 SAFETY CHECK (prevents 500 error)
        if not obj.owner:
            return None

        return {
            "id": getattr(obj.owner, "id", None),
            "name": getattr(obj.owner, "username", ""),
            "email": getattr(obj.owner, "email", ""),
        }