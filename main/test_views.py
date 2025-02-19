from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Petsitter, City, Region
from orders.models import Order
from pet.models import Pet, Category, Breed
from datetime import datetime, timedelta
User = get_user_model()

class MainViewsTest(TestCase):
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

        cls.petsitter_client = Client()
        cls.petsitter_client.force_login(cls.petsitter_user)

        cls.petsitter = Petsitter.objects.create(
            user=cls.petsitter_user,
            experience="Меньше 1 года",
            min_price=1000
        )

        # Создание тестового питомца
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

    def test_index_view(self):
        """Тест главной страницы"""
        response = self.guest_client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_petsitter_list_view(self):
        """Тест списка петситтеров"""
        response = self.guest_client.get(reverse('main:show_petsitters'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/petsitters_list.html')
        self.assertIn('filter', response.context)

    def test_user_profile_view(self):
        """Тест профиля пользователя"""
        response = self.auth_client.get(
            reverse('main:user_profile', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/user_profile.html')
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('pets', response.context)

    def test_petsitter_profile_view(self):
        """Тест профиля петситтера"""
        response = self.guest_client.get(
            reverse('main:petsitter_profile', args=[self.petsitter_user.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/petsitter_profile.html')
        self.assertEqual(response.context['petsitter'], self.petsitter)

    def test_applications_list_view(self):
        """Тест списка заявок"""
        # Тест доступа владельца
        response = self.auth_client.get(
            reverse('main:applications', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/applications_list.html')
        self.assertIn('object_list', response.context)

        # Тест доступа другого пользователя - должен получить 403
        response = self.petsitter_client.get(
            reverse('main:applications', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 403)

        # Тест с фильтром "petsitter" для владельца
        response = self.auth_client.get(
            reverse('main:applications', args=[self.user.username]) + '?filter=petsitter'
        )
        self.assertEqual(response.status_code, 200)

    def test_application_detail_view(self):
        """Тест детального просмотра заявки"""
        response = self.auth_client.get(
            reverse('main:application_detail', 
                   args=[self.user.username, self.order.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/application_detail.html')

    def test_accept_application(self):
        """Тест принятия заявки"""
        response = self.auth_client.get(
            reverse('main:accept_application', args=[self.order.id])
        )
        self.assertEqual(response.status_code, 302)
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'accepted')

    def test_reject_application(self):
        """Тест отклонения заявки"""
        response = self.auth_client.get(
            reverse('main:reject_application', args=[self.order.id])
        )
        self.assertEqual(response.status_code, 302)
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'rejected')

    def test_unauthorized_access(self):
        """Тест доступа неавторизованных пользователей"""
        urls = [
            reverse('main:applications', args=[self.user.username]),
            reverse('main:application_detail', 
                   args=[self.user.username, self.order.id]),
            reverse('main:accept_application', args=[self.order.id]),
            reverse('main:reject_application', args=[self.order.id])
        ]
        
        for url in urls:
            response = self.guest_client.get(url)
            self.assertIn(response.status_code, [302, 403])

    def tearDown(self):
        """Очистка данных после тестов"""
        Order.objects.all().delete()
        Pet.objects.all().delete()
        Breed.objects.all().delete()
        Category.objects.all().delete()
        Petsitter.objects.all().delete()
        User.objects.all().delete()
        City.objects.all().delete() 