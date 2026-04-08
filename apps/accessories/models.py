from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Accessory(models.Model):
    CATEGORY_CHOICES = [
        ("interior", "Interior"),
        ("exterior", "Exterior"),
        ("electronics", "Electronics"),
        ("safety", "Safety"),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accessories")

    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=1)

    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    is_approved = models.BooleanField(default=False)  # 🔥 admin approval

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AccessoryImage(models.Model):
    accessory = models.ForeignKey(
        Accessory, on_delete=models.CASCADE, related_name="images"
    )
    image = models.URLField()

    def __str__(self):
        return f"Image for {self.accessory.name}"