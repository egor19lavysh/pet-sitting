from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from pet.models import Category, Breed, Pet
from .models import Order
from datetime import datetime, timedelta
from .forms import OrderForm
from .schema import OrderSchema

User = get_user_model()


class OrdersViewsTest(TestCase):
    """
    Класс для тестирования view-функций приложения orders
    """

    @classmethod
    def setUpTestData(cls):
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

        cls.pet = Pet.objects.create(name="Шарик",
                                     age=2.5,
                                     category=cls.category,
                                     breed=cls.breed,
                                     owner=cls.user,
                                     weight=15,
                                     info="smth"
                                     )

        cls.order = Order.objects.create(
            name="Персик",
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

    def test_create_order_get_request(self):
        response = self.auth_client.get(reverse("orders:create_order", args=[self.petsitter.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], OrderForm)

        response = self.not_auth_client.get(reverse("orders:create_order", args=[self.petsitter.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login") + f"?next=/orders/create/{self.petsitter.id}")

    def test_create_order_get_request_with_pet_id(self):
        response = self.auth_client.get(reverse("pet:save_pet_id", args=[self.pet.id]))
        self.assertEqual(response.status_code, 302, msg="Тест функции для выбора id питомца")

        response = self.auth_client.get(reverse("orders:create_order", args=[self.petsitter.id]))
        self.assertEqual(response.status_code, 200, msg="Тест функции создания заказа")
        self.assertIsInstance(response.context["form"], OrderForm)

        form: OrderForm = response.context["form"]

        self.assertEqual(form.initial[OrderSchema.name], self.pet.name)
        self.assertEqual(form.initial[OrderSchema.category], self.category)
        self.assertEqual(form.initial[OrderSchema.breed], self.breed)
        self.assertEqual(form.initial[OrderSchema.age], self.pet.age)
        self.assertEqual(form.initial[OrderSchema.weight], self.pet.weight)
        self.assertEqual(form.initial[OrderSchema.certificate], self.pet.certificate)
        self.assertEqual(form.initial[OrderSchema.info], self.pet.info)

    def test_create_order_post_request(self):
        data = {
            OrderSchema.name: "Катюха",
            OrderSchema.category: self.category.id,
            OrderSchema.breed: self.breed.id,
            OrderSchema.age: 10.5,
            OrderSchema.weight: 22,
            OrderSchema.info: "Котопес",
            OrderSchema.walking: 3,
            OrderSchema.place: Order.HomeChoices.PETSITTER_HOME,
            OrderSchema.first_day: datetime.today().date(),
            OrderSchema.last_day: datetime.today().date() + timedelta(days=5),
            OrderSchema.price: 500
        }

        response = self.auth_client.post(reverse("orders:create_order", args=[self.petsitter.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main:index"))
        self.assertEqual(Order.objects.count(), 2)
        self.assertIsInstance(Order.objects.get(name="Катюха"), Order)

        response = self.not_auth_client.post(reverse("orders:create_order", args=[self.petsitter.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login") + f"?next=/orders/create/{self.petsitter.id}")

    def test_create_order_post_request_invalid_data(self):
        data = {
            OrderSchema.name: True,
            OrderSchema.category: self.category.id,
            OrderSchema.breed: self.breed.id,
            OrderSchema.age: -1,
            OrderSchema.weight: 22,
            OrderSchema.info: "Котопес",
            OrderSchema.walking: 3,
            OrderSchema.place: "Order.HomeChoices.PETSITTER_HOME",
            OrderSchema.first_day: datetime.today().date(),
            OrderSchema.last_day: datetime.today().date() + timedelta(days=5),
            OrderSchema.price: 500
        }

        response = self.auth_client.post(reverse("orders:create_order", args=[self.petsitter.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/create.html")
        self.assertIsInstance(response.context["form"], OrderForm)
