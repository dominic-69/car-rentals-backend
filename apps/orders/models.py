from django.db import models
from django.conf import settings
from apps.accessories.models import Accessory

User = settings.AUTH_USER_MODEL


# ======================
# 🛒 CART (ONE PER USER)
# ======================
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s Cart"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())


# ======================
# 🛒 CART ITEM
# ======================
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    accessory = models.ForeignKey(
        Accessory,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "accessory")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.cart.user} - {self.accessory.name} ({self.quantity})"

    def get_subtotal(self):
        return self.quantity * self.accessory.price


# ======================
# ❤️ WISHLIST
# ======================
class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )
    accessory = models.ForeignKey(
        Accessory,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "accessory")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} ❤️ {self.accessory.name}"


# ======================
# 🧾 ORDER
# ======================
class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    # 🔥 DELIVERY DETAILS (with defaults to avoid migration issues)
    name = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=15, default="")
    address = models.TextField(default="")
    city = models.CharField(max_length=100, default="")
    pincode = models.CharField(max_length=10, default="")

    # 💳 PAYMENT
    payment_id = models.CharField(max_length=255, null=True, blank=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

    def calculate_total(self):
        return sum(item.get_subtotal() for item in self.items.all())


# ======================
# 📦 ORDER ITEM
# ======================
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    accessory = models.ForeignKey(
        Accessory,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} - {self.accessory.name}"

    def get_subtotal(self):
        return self.quantity * self.price