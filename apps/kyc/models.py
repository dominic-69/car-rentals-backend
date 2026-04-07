from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class KYC(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100)

    license_image = models.URLField()
    selfie_image = models.URLField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    submitted_at = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.status}"