from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.dateparse import parse_date

from apps.cars.models import Car
from .models import Booking


# =========================
# 🔥 CREATE BOOKING
# =========================
class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        car_id = request.data.get("car_id")
        start_date = parse_date(request.data.get("start_date"))
        end_date = parse_date(request.data.get("end_date"))

        # ❌ VALIDATION
        if not car_id or not start_date or not end_date:
            return Response({"error": "Missing fields ❌"}, status=400)

        if start_date > end_date:
            return Response({"error": "Invalid date range ❌"}, status=400)

        # 🔍 GET CAR
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found ❌"}, status=404)

        # 🔥 CHECK OVERLAP (ONLY CONFIRMED BOOKINGS)
        conflict = Booking.objects.filter(
            car=car,
            start_date__lte=end_date,
            end_date__gte=start_date,
            status="confirmed"
        ).exists()

        if conflict:
            return Response({
                "error": "Car already booked for selected dates ❌"
            }, status=400)

        # 💰 CALCULATE PRICE
        days = (end_date - start_date).days or 1
        total_price = days * float(car.price)

        # ✅ CREATE BOOKING
        booking = Booking.objects.create(
            user=user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            payment_status="pending",
            status="pending"
        )

        return Response({
            "message": "Booking created",
            "booking_id": booking.id,
            "amount": total_price
        })


# =========================
# 🔥 PAYMENT SUCCESS
# =========================
class PaymentSuccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get("booking_id")

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found ❌"}, status=404)

        booking.payment_status = "paid"
        booking.status = "confirmed"
        booking.save()

        return Response({"message": "Booking confirmed ✅"})


# =========================
# 🔥 GET BOOKED DATES
# =========================
class CarAvailabilityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, car_id):
        bookings = Booking.objects.filter(
            car_id=car_id,
            status="confirmed"   # 🔥 IMPORTANT FIX
        )

        data = []

        for b in bookings:
            data.append({
                "start_date": b.start_date,
                "end_date": b.end_date
            })

        return Response({
            "booked_dates": data
        })
        
# =========================
# 🔥 MY BOOKINGS
# =========================
from rest_framework.permissions import IsAuthenticated

class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).order_by("-created_at")

        data = []

        for b in bookings:
            data.append({
                "id": b.id,
                "car": {
                    "title": b.car.title,
                    "image": b.car.images.first().image if b.car.images.exists() else None
                },
                "start_date": b.start_date,
                "end_date": b.end_date,
                "total_price": b.total_price,
                "status": b.status,
                "payment_status": b.payment_status,
            })

        return Response(data)
    
# =========================
# 🔥 CANCEL BOOKING
# =========================
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found ❌"}, status=404)

        if booking.status == "cancelled":
            return Response({"error": "Already cancelled ❌"}, status=400)

        booking.status = "cancelled"
        booking.save()

        return Response({"message": "Booking cancelled ✅"})