from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
# models.py

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")

    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    location = models.CharField(max_length=255)
    description = models.TextField()

    registration_number = models.CharField(max_length=50, unique=True, default="TEMP123")

    is_available = models.BooleanField(default=True)

    fuel_type = models.CharField(max_length=50, default="Petrol")
    transmission = models.CharField(max_length=50, default="Manual")
    seats = models.IntegerField(default=4)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.URLField()

    def __str__(self):
        return f"Image for {self.car.title}"