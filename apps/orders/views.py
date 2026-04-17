from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, Wishlist
from apps.accessories.models import Accessory


# ======================
# 🛒 ADD TO CART
# ======================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from apps.accessories.models import Accessory


class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            accessory = Accessory.objects.get(id=id)
        except Accessory.DoesNotExist:
            return Response({"error": "Accessory not found ❌"}, status=404)

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            accessory=accessory
        )

        if not created:
            cart.quantity += 1
            cart.save()

        return Response({"message": "Added to cart 🛒"})


# ======================
# 🛒 GET CART
# ======================
class MyCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)

        data = []
        total = 0

        for item in cart_items:
            subtotal = item.quantity * item.accessory.price
            total += subtotal

            data.append({
                "id": item.accessory.id,
                "name": item.accessory.name,
                "price": item.accessory.price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

        return Response({
            "items": data,
            "total": total
        })


# ======================
# ❌ REMOVE CART
# ======================
class RemoveCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        Cart.objects.filter(user=request.user, accessory_id=id).delete()
        return Response({"message": "Removed from cart ❌"})


# ======================
# ❤️ ADD TO WISHLIST
# ======================
class AddToWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        accessory = Accessory.objects.get(id=id)

        Wishlist.objects.get_or_create(
            user=request.user,
            accessory=accessory
        )

        return Response({"message": "Added to wishlist ❤️"})


# ======================
# ❤️ GET WISHLIST
# ======================
class MyWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)

        data = []
        for item in wishlist:
            data.append({
                "id": item.accessory.id,
                "name": item.accessory.name,
                "price": item.accessory.price
            })

        return Response(data)


# ======================
# ❌ REMOVE WISHLIST
# ======================
class RemoveWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        Wishlist.objects.filter(user=request.user, accessory_id=id).delete()
        return Response({"message": "Removed from wishlist ❌"})