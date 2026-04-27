from django.db import models
from django.conf import settings
from apps.cars.models import Car

User = settings.AUTH_USER_MODEL


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    # 🕐 NEW TIME FIELDS
    pickup_time = models.TimeField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)

    actual_return_time = models.DateTimeField(null=True, blank=True)

    # 💰 PRICE
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # 💸 FINE
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.car}"