from apps.cars.models import Car

def smart_car_search(message):
    qs = Car.objects.filter(is_available=True)

    message = message.lower()

    # price filter
    if "lakh" in message:
        import re
        match = re.search(r'(\d+)\s*lakh', message)
        if match:
            price = int(match.group(1)) * 100000
            qs = qs.filter(price__lte=price)

    # fuel
    if "petrol" in message:
        qs = qs.filter(fuel_type__iexact="petrol")

    if "diesel" in message:
        qs = qs.filter(fuel_type__iexact="diesel")

    # location
    if "kochi" in message:
        qs = qs.filter(location__icontains="kochi")

    return qs[:5]