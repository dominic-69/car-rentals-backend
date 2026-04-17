from django.db import models
from django.conf import settings
from apps.accessories.models import Accessory

User = settings.AUTH_USER_MODEL


# ❤️ WISHLIST
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "accessory")

    def __str__(self):
        return f"{self.user} - {self.accessory.name}"


# 🛒 CART
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "accessory")

    def __str__(self):
        return f"{self.user} - {self.accessory.name}"   