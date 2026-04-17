from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.cars.models import Car
from .models import Booking
from .utils import is_car_available


class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        car_id = request.data.get("car_id")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found ❌"}, status=404)

        # 🔥 CHECK AVAILABILITY
        if not is_car_available(car, start_date, end_date):
            return Response({"error": "Car not available for selected dates ❌"}, status=400)

        booking = Booking.objects.create(
            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            status="confirmed"
        )

        return Response({
            "message": "Booking successful ✅",
            "booking_id": booking.id
        })