from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem, Wishlist, Order, OrderItem
from apps.accessories.models import Accessory

import razorpay
from django.conf import settings


# ======================
# 🔧 IMAGE HELPER
# ======================
def get_image(accessory):
    try:
        images = accessory.images.all()

        if images.exists():
            img = images[0]

            # 🔥 IMPORTANT
            if hasattr(img.image, "url"):
                return img.image.url

            return str(img.image)

    except Exception as e:
        print("IMAGE ERROR:", e)

    return ""


# ======================
# 🛒 ADD TO CART
# ======================
class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        accessory = Accessory.objects.filter(id=id).first()
        if not accessory:
            return Response({"error": "Accessory not found"}, status=404)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            accessory=accessory
        )

        if not created:
            item.quantity += 1
            item.save()

        return Response({"message": "Added to cart", "quantity": item.quantity})


# ======================
# 🛒 GET CART
# ======================
class MyCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        items = CartItem.objects.filter(cart=cart).select_related("accessory").prefetch_related("accessory__images")

        data = []
        total = 0

        for item in items:
            accessory = item.accessory
            subtotal = item.quantity * accessory.price
            total += subtotal

            data.append({
                "cart_item_id": item.id,
                "id": accessory.id,
                "name": accessory.name,
                "price": accessory.price,
                "quantity": item.quantity,
                "subtotal": subtotal,
                "image": get_image(accessory),
            })

        return Response({"items": data, "total": total})


# ======================
# 🔼 INCREASE
# ======================
class IncreaseQuantity(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        item = CartItem.objects.filter(
            cart__user=request.user,
            accessory_id=id
        ).first()

        if not item:
            return Response({"error": "Item not found"}, status=404)

        item.quantity += 1
        item.save()
        return Response({"quantity": item.quantity})


# ======================
# 🔽 DECREASE
# ======================
class DecreaseQuantity(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        item = CartItem.objects.filter(
            cart__user=request.user,
            accessory_id=id
        ).first()

        if not item:
            return Response({"error": "Item not found"}, status=404)

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

        return Response({"message": "Updated"})


# ======================
# ❌ REMOVE
# ======================
class RemoveCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        CartItem.objects.filter(
            cart__user=request.user,
            accessory_id=id
        ).delete()

        return Response({"message": "Removed"})


# ======================
# ❤️ WISHLIST
# ======================
class AddToWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        accessory = Accessory.objects.filter(id=id).first()
        if not accessory:
            return Response({"error": "Not found"}, status=404)

        Wishlist.objects.get_or_create(user=request.user, accessory=accessory)
        return Response({"message": "Added to wishlist"})


class MyWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []

        items = Wishlist.objects.filter(user=request.user).select_related("accessory").prefetch_related("accessory__images")

        for item in items:
            data.append({
                "id": item.accessory.id,
                "name": item.accessory.name,
                "price": item.accessory.price,
                "image": get_image(item.accessory)
            })

        return Response(data)


class RemoveWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        Wishlist.objects.filter(
            user=request.user,
            accessory_id=id
        ).delete()

        return Response({"message": "Removed"})


# ======================
# 💳 CREATE RAZORPAY ORDER
# ======================
class CreateRazorpayOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            return Response({"error": "Cart empty"}, status=400)

        total = sum(item.quantity * item.accessory.price for item in cart.items.all())
        amount = int(total * 100)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        return Response({
            "order_id": order["id"],
            "amount": amount,
            "key": settings.RAZORPAY_KEY_ID
        })


# ======================
# 🧾 CHECKOUT (MAIN FIX)
# ======================
class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart:
            return Response({"error": "Cart not found"}, status=404)

        items = cart.items.all()
        if not items.exists():
            return Response({"error": "Cart empty"}, status=400)

        order = Order.objects.create(
            user=request.user,
            name=request.data.get("name"),
            phone=request.data.get("phone"),
            address=request.data.get("address"),
            city=request.data.get("city"),
            pincode=request.data.get("pincode"),
            payment_id=request.data.get("payment_id"),
        )

        total = 0

        for item in items:
            subtotal = item.quantity * item.accessory.price
            total += subtotal

            OrderItem.objects.create(
                order=order,
                accessory=item.accessory,
                quantity=item.quantity,
                price=item.accessory.price
            )

        order.total_price = total
        order.save()

        items.delete()  # 🔥 CLEAR CART

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id
        })


# ======================
# 📜 USER ORDERS
# ======================
class MyOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []

        orders = Order.objects.filter(user=request.user).prefetch_related("items__accessory__images")

        for order in orders:
            items = []

            for item in order.items.all():
                items.append({
                    "name": item.accessory.name,
                    "price": item.price,
                    "quantity": item.quantity,
                    "image": get_image(item.accessory)
                })

            data.append({
                "order_id": order.id,
                "total": order.total_price,
                "status": order.status,
                "items": items
            })

        return Response(data)


# ======================
# 🧑‍💼 ADMIN ORDERS
# ======================
class AdminOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_staff or getattr(request.user, "role", None) == "admin"):
            return Response({"error": "Unauthorized"}, status=403)

        data = []

        orders = Order.objects.all().prefetch_related("items__accessory__images")

        for order in orders:
            items = []

            for it in order.items.all():
                items.append({
                    "name": it.accessory.name,
                    "price": it.price,
                    "quantity": it.quantity,
                    "image": get_image(it.accessory)
                })

            data.append({
                "id": order.id,
                "user": str(order.user),
                "total": order.total_price,
                "status": order.status,
                "items": items
            })

        return Response(data)


# ======================
# 🔄 UPDATE STATUS
# ======================
class UpdateOrderStatus(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        if not (request.user.is_staff or getattr(request.user, "role", None) == "admin"):
            return Response({"error": "Unauthorized"}, status=403)

        order = Order.objects.filter(id=id).first()

        if not order:
            return Response({"error": "Not found"}, status=404)

        if order.status in ["DELIVERED", "CANCELLED"]:
            return Response({"error": "Status locked"}, status=400)

        order.status = request.data.get("status")
        order.save()

        return Response({"message": "Updated"})