from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Accessory

User = get_user_model()


class AccessoryTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # 🔥 create user (seller)
        self.user = User.objects.create_user(
            username="seller",
            password="123456",
            role="seller"
        )

        # 🔥 login
        self.client.force_authenticate(user=self.user)

    # =========================
    # 🔥 TEST CREATE ACCESSORY
    # =========================
    def test_create_accessory(self):
        url = "/api/accessories/create/"

        data = {
            "name": "Car Cover",
            "brand": "AutoPro",
            "price": 1000,
            "stock": 5,
            "description": "Waterproof cover",
            "category": "exterior"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Accessory.objects.count(), 1)

    # =========================
    # 🔥 TEST LIST ACCESSORIES
    # =========================
    def test_list_accessories(self):
        Accessory.objects.create(
            seller=self.user,
            name="Seat Cover",
            brand="Auto",
            price=500,
            stock=10,
            description="Good",
            category="interior",
            is_approved=True
        )

        url = "/api/accessories/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # =========================
    # 🔥 TEST UNAUTHORIZED CREATE
    # =========================
    def test_unauthorized_create(self):
        self.client.logout()

        url = "/api/accessories/create/"
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 401)

    # =========================
    # 🔥 TEST MY ACCESSORIES
    # =========================
    def test_my_accessories(self):
        Accessory.objects.create(
            seller=self.user,
            name="Mirror",
            brand="Auto",
            price=200,
            stock=3,
            description="Side mirror",
            category="exterior"
        )

        url = "/api/accessories/my/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)