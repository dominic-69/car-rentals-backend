from .models import Booking


def is_car_available(car, start_date, end_date):
    overlapping = Booking.objects.filter(
        car=car,
        start_date__lte=end_date,
        end_date__gte=start_date,
        status="confirmed"
    )

    return not overlapping.exists()