from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "brand", "price", "owner", "is_available")
    list_filter = ("brand", "is_available")
    search_fields = ("title", "brand", "location")