from rest_framework import generics, permissions
from .models import Car
from .serializers import CarSerializer
from .permissions import IsSeller, IsOwner
import cloudinary.uploader
from .models import Car, CarImage

class MyCarsView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)
    
    
# views.py



from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Car, CarImage
from .serializers import CarSerializer
from .permissions import IsSeller
import cloudinary.uploader


class CarCreateView(generics.CreateAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def perform_create(self, serializer):
        car = serializer.save(owner=self.request.user)

        images = self.request.FILES.getlist("images")

        # 🔥 SAFE CHECK
        if images:
            if len(images) > 5:
                raise Exception("Max 5 images allowed")

            for img in images:
                upload = cloudinary.uploader.upload(img, folder="cars")

                CarImage.objects.create(
                    car=car,
                    image=upload["secure_url"]
                )

class CarListView(generics.ListAPIView):
    queryset = Car.objects.filter(is_available=True)
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]


class CarDetailView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]


class CarUpdateView(generics.UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"


class CarDeleteView(generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"