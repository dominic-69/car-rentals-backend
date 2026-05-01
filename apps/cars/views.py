from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from django.db import IntegrityError
from django.db.models import Avg

from .models import Car, CarImage
from .serializers import CarSerializer
from .permissions import IsSeller, IsOwner

from apps.rental.utils import is_car_available

import cloudinary.uploader
import requests

# Function: Location to Lat/Lng
def get_lat_lng(location):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location,
            "format": "json"
        }
        headers = {
            "User-Agent": "car-app"
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])

    except Exception as e:
        print("Geocoding error:", e)

    return None, None

# Create Car View
class CreateCarView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request):
        data = request.data

        try:
            # Duplicate check
            if Car.objects.filter(
                registration_number=data.get("registration_number")
            ).exists():
                return Response({"error": "Car already exists ❌"}, status=400)

            # Lat/Lng from frontend
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            try:
                latitude = float(latitude) if latitude else None
                longitude = float(longitude) if longitude else None
            except:
                latitude = None
                longitude = None

            # Auto convert location to Lat/Lng
            if not latitude or not longitude:
                lat, lng = get_lat_lng(data.get("location"))

                if lat and lng:
                    latitude = lat
                    longitude = lng

            # Safe numbers
            try:
                price = float(data.get("price", 0))
            except:
                return Response({"error": "Invalid price ❌"}, status=400)

            try:
                seats = int(data.get("seats", 4))
            except:
                seats = 4

            # Create car object
            car = Car.objects.create(
                owner=request.user,
                title=data.get("title"),
                brand=data.get("brand"),
                price=price,
                location=data.get("location"),
                registration_number=data.get("registration_number"),
                description=data.get("description"),
                fuel_type=data.get("fuel_type", "petrol"),
                transmission=data.get("transmission", "manual"),
                seats=seats,
                latitude=latitude,
                longitude=longitude,
                status="approved",
                car_type="rental"
            )

            # Handle images
            images = request.FILES.getlist("images")

            if len(images) > 5:
                return Response({"error": "Max 5 images ❌"}, status=400)

            for img in images:
                try:
                    upload = cloudinary.uploader.upload(img)
                    url = upload.get("secure_url")

                    if url:
                        CarImage.objects.create(car=car, image=url)

                except Exception as e:
                    print("Cloudinary error:", e)

            return Response({
                "message": "Car added successfully 🚗",
                "latitude": latitude,
                "longitude": longitude
            })

        except Exception as e:
            print("FINAL ERROR:", str(e))
            return Response({"error": str(e)}, status=500)

# Seller - My Cars
class MyCarsView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)

# Rental Page Home
class CarListView(APIView):
    def get(self, request):
        cars = Car.objects.filter(
            status="approved",
            car_type="rental"
        ).order_by("-created_at")

        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

# Car Detail
class CarDetailView(APIView):
    def get(self, request, id):
        try:
            car = Car.objects.get(id=id, status="approved")
        except Car.DoesNotExist:
            return Response({"error": "Car not found ❌"}, status=404)

        serializer = CarSerializer(car)
        return Response(serializer.data)

# Update Car
class CarUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, id):
        try:
            car = Car.objects.get(id=id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        if car.owner != request.user:
            return Response({"error": "Unauthorized"}, status=403)

        data = request.data

        if Car.objects.filter(
            registration_number=data.get("registration_number")
        ).exclude(id=car.id).exists():
            return Response({"error": "Registration exists ❌"}, status=400)

        car.title = data.get("title", car.title)
        car.brand = data.get("brand", car.brand)
        car.price = data.get("price", car.price)
        car.location = data.get("location", car.location)
        car.registration_number = data.get("registration_number", car.registration_number)
        car.description = data.get("description", car.description)
        car.fuel_type = data.get("fuel_type", car.fuel_type)
        car.transmission = data.get("transmission", car.transmission)
        car.seats = data.get("seats", car.seats)

        car.status = "pending"
        car.save()

        images = request.FILES.getlist("images")

        if images:
            if len(images) > 5:
                return Response({"error": "Max 5 images ❌"}, status=400)

            CarImage.objects.filter(car=car).delete()

            for img in images:
                upload = cloudinary.uploader.upload(img)
                CarImage.objects.create(car=car, image=upload["secure_url"])

        return Response({"message": "Updated (Pending approval)"})

# Delete Car
class CarDeleteView(generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"

# Search (Rental Only)
@api_view(["GET"])
def search_cars(request):
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    cars = Car.objects.filter(
        is_available=True,
        status="approved",
        car_type="rental"
    )

    if max_price:
        cars = cars.filter(price__lte=max_price)

    data = []

    for car in cars:
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

# Sell Car (Marketplace)
class CreateSellCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        if Car.objects.filter(
            registration_number=data.get("registration_number")
        ).exists():
            return Response({"error": "Car exists ❌"}, status=400)

        try:
            car = Car.objects.create(
                owner=request.user,
                title=data.get("title"),
                brand=data.get("brand"),
                price=data.get("price"),
                location=data.get("location"),
                description=data.get("description"),
                registration_number=data.get("registration_number"),
                fuel_type=data.get("fuel_type", "petrol"),
                transmission=data.get("transmission", "manual"),
                status="pending",
                car_type="sale"
            )
        except IntegrityError:
            return Response({"error": "Registration exists ❌"}, status=400)

        images = request.FILES.getlist("images")

        if not images:
            return Response({"error": "Upload at least 1 image ❌"}, status=400)

        if len(images) > 5:
            return Response({"error": "Max 5 images ❌"}, status=400)

        for img in images:
            upload = cloudinary.uploader.upload(img)
            CarImage.objects.create(car=car, image=upload["secure_url"])

        return Response({"message": "Submitted for approval ⏳"})

# Buy Page (Sale Only)
class ApprovedCarsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cars = Car.objects.filter(
            status="approved",
            car_type="sale"
        )

        data = []
        for car in cars:
            data.append({
                "id": car.id,
                "title": car.title,
                "brand": car.brand,
                "price": car.price,
                "location": car.location,
                "fuel_type": car.fuel_type,
                "description": car.description,
                "seller": {
                    "id": car.owner.id,
                    "name": car.owner.username,
                    "email": car.owner.email,
                },
                "images": [
                    {"image": img.image} for img in car.images.all()
                ]
            })

        return Response(data)

# Admin - Pending Cars
class AdminPendingCarsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"error": "Unauthorized ❌"}, status=403)

        cars = Car.objects.filter(status="pending")
        data = []

        for car in cars:
            data.append({
                "id": car.id,
                "title": car.title,
                "owner": car.owner.username,
                "price": car.price,
                "fuel_type": car.fuel_type,
                "images": [
                    {"id": img.id, "image": img.image}
                    for img in car.images.all()
                ]
            })

        return Response(data)

# Admin Approve / Reject
class AdminApproveCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, car_id):
        if request.user.role != "admin":
            return Response({"error": "Unauthorized ❌"}, status=403)

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        action = request.data.get("action")

        if action == "approve":
            car.status = "approved"
        elif action == "reject":
            car.status = "rejected"
        else:
            return Response({"error": "Invalid action"}, status=400)

        car.save()
        return Response({"message": f"Car {action}d ✅"})

# Chatbot View
class ChatbotView(APIView):
    def post(self, request):
        message = request.data.get("message")
        try:
            res = requests.post(
                "http://127.0.0.1:8001/chat/",
                json={"message": message}
            )
            return Response(res.json())
        except Exception as e:
            return Response({"error": "FastAPI not working ❌"})

# Price Suggestion View
class PriceSuggestionView(APIView):
    def post(self, request):
        brand = request.data.get("brand")
        fuel_type = request.data.get("fuel_type")
        seats = request.data.get("seats")

        cars = Car.objects.filter(
            status="approved",
            car_type="rental"
        )

        if brand:
            cars = cars.filter(brand__icontains=brand)
        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)
        if seats:
            try:
                cars = cars.filter(seats=int(seats))
            except:
                pass

        if not cars.exists():
            return Response({
                "suggested_price": 2000,
                "min": 1500,
                "max": 2500,
                "message": "No similar cars found"
            })

        avg_price = cars.aggregate(avg=Avg("price"))["avg"]
        avg_price = float(avg_price)

        return Response({
            "suggested_price": round(avg_price, 2),
            "min": round(avg_price * 0.8, 2),
            "max": round(avg_price * 1.2, 2),
        })

# External API Utils
def call_fastapi_price(data):
    try:
        res = requests.post(
            "http://127.0.0.1:8001/predict-price",
            json=data
        )
        return res.json()
    except Exception as e:
        return None