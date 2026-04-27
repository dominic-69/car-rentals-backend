from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.dateparse import parse_date, parse_time


from apps.cars.models import Car
from .models import Booking


 
 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date, parse_time

from apps.cars.models import Car
from .models import Booking


class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        car_id = request.data.get("car_id")
        start_date = parse_date(request.data.get("start_date"))
        end_date = parse_date(request.data.get("end_date"))

        # 🕐 SAFE TIME INPUTS (FIXED)
        pickup_time_raw = request.data.get("pickup_time")
        return_time_raw = request.data.get("return_time")

        pickup_time = parse_time(pickup_time_raw) if pickup_time_raw else None
        return_time = parse_time(return_time_raw) if return_time_raw else None

        # ❌ VALIDATION
        if not car_id or not start_date or not end_date:
            return Response({"error": "Missing date fields ❌"}, status=400)

        if not pickup_time or not return_time:
            return Response({"error": "Pickup and return time required ❌"}, status=400)

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
            pickup_time=pickup_time,
            return_time=return_time,
            total_price=total_price,
            payment_status="pending",
            status="pending"
        )

        return Response({
            "message": "Booking created ✅",
            "booking_id": booking.id,
            "amount": total_price,
            "pickup_time": str(pickup_time),
            "return_time": str(return_time)
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
    
    
# =========================
# 🔥 SELLER BOOKINGS
# =========================
class SellerBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "seller":
            return Response({"error": "Unauthorized ❌"}, status=403)

        bookings = Booking.objects.filter(
            car__owner=request.user
        ).order_by("-created_at")

        data = []

        for b in bookings:
            data.append({
                "id": b.id,
                "user": {
                    "name": b.user.username,
                    "email": b.user.email,
                },
                "car": b.car.title,
                "start_date": b.start_date,
                "end_date": b.end_date,
                "status": b.status,
                "payment_status": b.payment_status,
                "total_price": b.total_price,
            })

        return Response(data)
    
# =========================
# 🔥 ADMIN BOOKINGS
# =========================
# =========================
# 🔥 ADMIN BOOKINGS (READ ONLY)
# =========================
class AdminBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"error": "Unauthorized ❌"}, status=403)

        bookings = Booking.objects.select_related(
            "user", "car__owner"
        ).prefetch_related("car__images").order_by("-created_at")

        data = []

        for b in bookings:
            data.append({
                "id": b.id,

                "user": {
                    "id": b.user.id,
                    "name": b.user.username,
                    "email": b.user.email,
                    "phone": b.user.phone,
                    "address": b.user.address,
                    "profile_image": b.user.profile_image.url if b.user.profile_image else None,
                },

                "car": {
                    "id": b.car.id,
                    "title": b.car.title,
                    "brand": b.car.brand,
                    "price": b.car.price,
                    "location": b.car.location,
                    "owner": b.car.owner.username,
                    "image": b.car.images.first().image if b.car.images.exists() else None,
                },

                "start_date": b.start_date,
                "end_date": b.end_date,
                "total_price": b.total_price,
                "status": b.status,
                "payment_status": b.payment_status,
                "created_at": b.created_at,
            })

        return Response(data)
    
# =========================
# 🔥 SELLER UPDATE BOOKING STATUS
# =========================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Booking

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



class SellerUpdateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        # 🔒 ROLE CHECK
        if request.user.role != "seller":
            return Response({"error": "Unauthorized ❌"}, status=403)

        # 🔍 GET BOOKING
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found ❌"}, status=404)

        # 🔐 OWNER CHECK
        if booking.car.owner != request.user:
            return Response({"error": "Not your car ❌"}, status=403)

        action = request.data.get("action")

        # 🎯 UPDATE STATUS
        if action == "confirm":
            booking.status = "confirmed"

        elif action == "cancel":
            booking.status = "cancelled"

        elif action == "complete":
            booking.status = "completed"

        else:
            return Response({"error": "Invalid action ❌"}, status=400)

        booking.save()

        # =========================
        # 🔥 REAL-TIME UPDATE
        # =========================
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "booking_updates",
            {
                "type": "booking_update",
                "message": f"Booking {booking.id} updated to {booking.status}",
            }
        )

        return Response({"message": "Booking updated ✅"})
    
from datetime import datetime
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ReturnCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        current_time = now()
        booking.actual_return_time = current_time

        # 🔥 Expected return datetime
        expected_return = datetime.combine(
            booking.end_date,
            booking.return_time
        )

        # 🔥 Calculate delay
        delay_hours = (current_time - expected_return).total_seconds() / 3600

        if delay_hours > 0:
            fine = round(delay_hours) * 250
            booking.fine_amount = fine

        booking.status = "completed"
        booking.save()

        return Response({
            "message": "Car returned successfully",
            "fine": booking.fine_amount
        })