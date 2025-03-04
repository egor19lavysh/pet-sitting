from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from users.models import Petsitter, City, Region
from orders.models import Order
from pet.models import Pet, Category, Breed
from datetime import datetime, timedelta
from main import views

User = get_user_model()

class MainUrlsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестовых пользователей
        cls.user = User.objects.create(
            username="test_user",
            password="test123",
            first_name="Test",
            last_name="User"
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        # Создание тестового петситтера
        cls.region = Region.objects.create(name="Test Region")
        cls.city = City.objects.create(name="Test City", region=cls.region)
        cls.petsitter_user = User.objects.create(
            username="petsitter",
            password="test456",
            is_petsitter=True,
            city=cls.city
        )
        cls.petsitter = Petsitter.objects.create(
            user=cls.petsitter_user,
            experience="Меньше 1 года",
            min_price=1000
        )
        cls.petsitter_client = Client()
        cls.petsitter_client.force_login(cls.petsitter_user)

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

        # Создание тестового заказа
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
            petsitter=cls.petsitter_user,
            first_day=datetime.today(),
            last_day=datetime.today() + timedelta(days=5),
            price=500.0
        )

        cls.guest_client = Client()

    def test_index_url(self):
        """Тест URL главной страницы"""
        url = reverse('main:index')
        self.assertEqual(resolve(url).func, views.index)
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_petsitter_list_url(self):
        """Тест URL списка петситтеров"""
        url = reverse('main:show_petsitters')
        self.assertEqual(resolve(url).func, views.petsitter_list)
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_petsitter_profile_url(self):
        """Тест URL профиля петситтера"""
        url = reverse('main:petsitter_profile', args=[self.petsitter_user.id])
        self.assertEqual(resolve(url).func, views.petsitter_profile)
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_url(self):
        """Тест URL профиля пользователя"""
        url = reverse('main:user_profile', args=[self.user.username])
        self.assertEqual(resolve(url).func, views.user_profile)
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_applications_list_url(self):
        """Тест URL списка заявок"""
        url = reverse('main:applications', args=[self.user.username])
        self.assertEqual(resolve(url).func, views.ApplicationsListView)
        
        # Проверка доступа владельца
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка доступа другого пользователя - должен получить 403
        response = self.petsitter_client.get(url)
        self.assertEqual(response.status_code, 403)
        
        # Проверка доступа неавторизованного пользователя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_application_detail_url(self):
        """Тест URL деталей заявки"""
        url = reverse('main:application_detail', args=[self.user.username, self.order.id])
        self.assertEqual(resolve(url).func.view_class, views.ApplicationDetailView)
        
        # Проверка доступа владельца
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_accept_application_url(self):
        """Тест URL принятия заявки"""
        url = reverse('main:accept_application', args=[self.order.id])
        self.assertEqual(resolve(url).func, views.accept_app_status)
        
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_reject_application_url(self):
        """Тест URL отклонения заявки"""
        url = reverse('main:reject_application', args=[self.order.id])
        self.assertEqual(resolve(url).func, views.reject_app_status)
        
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        """Очистка данных после тестов"""
        Order.objects.all().delete()
        Petsitter.objects.all().delete()
        User.objects.all().delete()
        City.objects.all().delete() 