from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "seller"


from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Car(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cars"
    )

    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    #   KEEP location
    location = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    registration_number = models.CharField(
        max_length=50,
        unique=True
    )

    is_available = models.BooleanField(default=True)

    CAR_TYPE_CHOICES = (
        ("rental", "Rental"),
        ("sale", "Sale"),
    )
    car_type = models.CharField(
        max_length=10,
        choices=CAR_TYPE_CHOICES,
        default="rental",
        db_index=True
    )

    FUEL_CHOICES = (
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("electric", "Electric"),
        ("hybrid", "Hybrid"),
        ("cng", "CNG"),
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        default="petrol"
    )

    TRANSMISSION_CHOICES = (
        ("manual", "Manual"),
        ("automatic", "Automatic"),
    )
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        default="manual"
    )

    seats = models.IntegerField(default=4)

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True
    )

    #  MAP  
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.registration_number}"


#   Cloudinary URL storage
class CarImage(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.URLField()

    def __str__(self):
        return f"Image for {self.car.title}"