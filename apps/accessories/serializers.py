from rest_framework import serializers
from .models import Accessory, AccessoryImage


class AccessoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoryImage
        fields = ["id", "image"]


class AccessorySerializer(serializers.ModelSerializer):
    images = AccessoryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Accessory
        fields = "__all__"