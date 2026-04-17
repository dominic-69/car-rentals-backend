from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.db import IntegrityError

from .models import Car, CarImage
from .serializers import CarSerializer
from .permissions import IsSeller, IsOwner

from apps.rental.utils import is_car_available  # 🔥 IMPORTANT

import cloudinary.uploader


# =========================
# 🔥 CREATE CAR
# =========================
class CreateCarView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request):
        data = request.data

        # ✅ DUPLICATE CHECK
        if Car.objects.filter(
            registration_number=data.get("registration_number")
        ).exists():
            return Response({
                "error": "Car with this registration number already exists ❌"
            }, status=400)

        try:
            car = Car.objects.create(
                owner=request.user,
                title=data.get("title"),
                brand=data.get("brand"),
                price=data.get("price"),
                location=data.get("location"),
                registration_number=data.get("registration_number"),
                description=data.get("description"),
                fuel_type=data.get("fuel_type", "Petrol"),
                transmission=data.get("transmission", "Manual"),
                seats=data.get("seats", 4),
            )
        except IntegrityError:
            return Response({
                "error": "Registration number already exists ❌"
            }, status=400)

        # 🔥 HANDLE IMAGES
        images = request.FILES.getlist("images")

        if len(images) > 5:
            return Response({"error": "Maximum 5 images allowed ❌"}, status=400)

        for img in images:
            upload = cloudinary.uploader.upload(img)
            CarImage.objects.create(
                car=car,
                image=upload["secure_url"]
            )

        return Response({"message": "Car added successfully 🚗"})


# =========================
# 🔥 SELLER → MY CARS
# =========================
class MyCarsView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)


# =========================
# 🔥 ALL CARS (PUBLIC)
# =========================
class CarListView(generics.ListAPIView):
    queryset = Car.objects.filter(is_available=True)
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]


# =========================
# 🔥 CAR DETAIL
# =========================
class CarDetailView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]


# =========================
# 🔥 UPDATE CAR
# =========================
class CarUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, id):
        try:
            car = Car.objects.get(id=id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        # 🔐 OWNER CHECK
        if car.owner != request.user:
            return Response({"error": "Unauthorized"}, status=403)

        data = request.data

        # ✅ DUPLICATE CHECK
        if Car.objects.filter(
            registration_number=data.get("registration_number")
        ).exclude(id=car.id).exists():
            return Response({
                "error": "Registration number already exists ❌"
            }, status=400)

        try:
            car.title = data.get("title", car.title)
            car.brand = data.get("brand", car.brand)
            car.price = data.get("price", car.price)
            car.location = data.get("location", car.location)
            car.registration_number = data.get("registration_number", car.registration_number)
            car.description = data.get("description", car.description)
            car.fuel_type = data.get("fuel_type", car.fuel_type)
            car.transmission = data.get("transmission", car.transmission)
            car.seats = data.get("seats", car.seats)

            car.save()

        except IntegrityError:
            return Response({
                "error": "Registration number already exists ❌"
            }, status=400)

        # 🔥 HANDLE IMAGES
        images = request.FILES.getlist("images")

        if images:
            if len(images) > 5:
                return Response({"error": "Maximum 5 images allowed ❌"}, status=400)

            CarImage.objects.filter(car=car).delete()

            for img in images:
                upload = cloudinary.uploader.upload(img)
                CarImage.objects.create(
                    car=car,
                    image=upload["secure_url"]
                )

        return Response({"message": "Car updated successfully ✅"})


# =========================
# 🔥 DELETE CAR
# =========================
class CarDeleteView(generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"


# =========================
# 🔥 SEARCH CARS (WITH AVAILABILITY)
# =========================
@api_view(["GET"])
def search_cars(request):
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    cars = Car.objects.filter(is_available=True)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    data = []

    for car in cars:
        # 🔥 CHECK AVAILABILITY
        if start_date and end_date:
            if not is_car_available(car, start_date, end_date):
                continue

        data.append({
            "id": car.id,
            "title": car.title,
            "price": float(car.price),
            "fuel": car.fuel_type,
            "location": car.location,
        })

    return Response(data)