from django.http import HttpResponseForbidden
from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from orders.models import Order
from pet.models import Category, Breed
from datetime import datetime, timedelta
from django.urls import reverse, resolve
from orders.views import *

User = get_user_model()


class OrdersUrlsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # set up users and clients
        cls.user = User.objects.create(
            username="test_user",
            password="password",
            first_name="Egor",
            last_name="Lavysh"
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        cls.other_user = User.objects.create(
            username="other_user",
            password="password2",
            first_name="Vasya",
            last_name="Pupkin"
        )
        cls.other_client = Client()
        cls.other_client.force_login(cls.other_user)

        cls.not_auth_client = Client()

        cls.petsitter = User.objects.create(
            username="test_petsitter",
            password="password"
        )

        # set up category, breed and order

        cls.category = Category.objects.create(name="Собака")
        cls.breed = Breed.objects.create(
            category=cls.category,
            name="Мопс"
        )

        cls.order = Order.objects.create(
            name="Шарик",
            category=cls.category,
            breed=cls.breed,
            age=3.5,
            weight=25.7,
            certificate=True,
            info="Хороший и послушный пес",
            walking=4,
            place=Order.HomeChoices.PETSITTER_HOME,
            owner=cls.user,
            petsitter=cls.petsitter,
            first_day=datetime.today(),
            last_day=datetime.today() + timedelta(days=5),
            price=500.0
        )

    def test_create_url(self):
        url = reverse('orders:create_order', args=[self.petsitter.id])
        self.assertEqual(resolve(url).func, create_order)

        response = self.auth_client.get(reverse("orders:create_order", args=[self.petsitter.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/create.html")

        response = self.not_auth_client.get(reverse("orders:create_order", args=[self.petsitter.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login") + f"?next=/orders/create/{self.petsitter.id}")

    def test_update_url(self):
        url = reverse('orders:update_order', args=[self.order.id])
        self.assertEqual(resolve(url).func.view_class, UpdateOrderView)

        response = self.auth_client.get(reverse("orders:update_order", args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_update_form.html")

        response = self.other_client.get(reverse("orders:update_order", args=[self.order.id]))
        self.assertEqual(response.status_code, 403)
        self.assertIsInstance(response, HttpResponseForbidden)

        response = self.not_auth_client.get(reverse("orders:update_order", args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login") + f"?next=/orders/update/{self.order.id}")

    def test_delete_url(self):
        url = reverse('orders:delete_order', args=[self.order.id])
        self.assertEqual(resolve(url).func.view_class, DeleteOrderView)

        response = self.other_client.get(reverse("orders:delete_order", args=[self.order.id]))
        self.assertEqual(response.status_code, 403)
        self.assertIsInstance(response, HttpResponseForbidden)

        response = self.not_auth_client.get(reverse("orders:delete_order", args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login") + f"?next=/orders/delete/{self.order.id}")

        response = self.auth_client.get(reverse("orders:delete_order", args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_confirm_delete.html")

    def tearDown(self) -> None:
        Order.objects.all().delete()
        Category.objects.all().delete()
        Breed.objects.all().delete()
        User.objects.all().delete()
