from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from check_system.models import PetsitterCheck, Report, Reject
from django.core.files.uploadedfile import SimpleUploadedFile
from orders.models import Order
from pet.models import Category, Breed
from datetime import datetime, timedelta
from check_system import views

User = get_user_model()

class CheckSystemUrlsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание пользователей
        cls.owner = User.objects.create_user(
            username='owner',
            password='testpass123',
            email='owner@example.com'
        )
        cls.owner_client = Client()
        cls.owner_client.force_login(cls.owner)
        
        cls.petsitter = User.objects.create_user(
            username='petsitter',
            password='testpass123',
            email='petsitter@example.com',
            is_petsitter=True
        )
        cls.petsitter_client = Client()
        cls.petsitter_client.force_login(cls.petsitter)

        cls.other_user = User.objects.create_user(
            username='other_user',
            password='testpass123'
        )
        cls.other_client = Client()
        cls.other_client.force_login(cls.other_user)

        # Создание категории и породы
        cls.category = Category.objects.create(name="Dog")
        cls.breed = Breed.objects.create(name="Labrador", category=cls.category)

        # Создание заказа
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
            owner=cls.owner,
            petsitter=cls.petsitter,
            first_day=datetime.today(),
            last_day=datetime.today() + timedelta(days=5),
            price=500.0
        )

        # Создание системы проверки
        cls.check_system = PetsitterCheck.objects.create(
            petsitter=cls.petsitter,
            owner=cls.owner,
            order=cls.order,
            frequency=3,
            interval=4,
            start_date=datetime.today(),
            end_date=datetime.today() + timedelta(days=5),
            start_time="12:00"
        )

        cls.image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        cls.video = SimpleUploadedFile(
            "test_video.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        # Создание отчета
        cls.report = Report.objects.create(
            petsitter_check=cls.check_system,
            text="Тестовый отчет",
            image=cls.image,
            video=cls.video
        )

        # Создание обращения
        cls.reject = Reject.objects.create(
            system=cls.check_system,
            text="Тестовое обращение"
        )

        cls.guest_client = Client()

    def test_show_all_url(self):
        """Тест URL списка всех систем проверки"""
        url = reverse('check_system:show_all')
        self.assertEqual(resolve(url).func, views.show_all)
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка для неавторизованного пользователя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={url}')

    def test_show_system_url(self):
        """Тест URL просмотра системы проверки"""
        url = reverse('check_system:show', args=[self.check_system.id])
        self.assertEqual(resolve(url).func, views.show)
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка для петситтера
        response = self.petsitter_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка для неавторизованного пользователя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={url}')

        


    def test_show_all_reports_url(self):
        """Тест URL списка всех отчетов"""
        url = reverse('check_system:show_all_reports', args=[self.check_system.id])
        self.assertEqual(resolve(url).func, views.show_all_reports)
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка для гостя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_show_report_url(self):
        """Тест URL просмотра отчета"""
        url = reverse('check_system:show_report', args=[self.report.id])
        self.assertEqual(resolve(url).func, views.show_report)
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка для гостя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 404)



    def test_activate_url(self):
        """Тест URL активации системы проверки"""
        url = reverse('check_system:activate', args=[self.order.id])
        self.assertEqual(resolve(url).func, views.activate)
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка для гостя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_load_report_url(self):
        """Тест URL загрузки отчета"""
        url = reverse('check_system:load_report', args=[self.check_system.id])
        self.assertEqual(resolve(url).func, views.load_report)
        
        # Проверка для петситтера
        response = self.petsitter_client.get(url)
        self.assertIn(response.status_code, [200, 404])  # Зависит от времени
        
        # Проверка для гостя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_stop_url(self):
        """Тест URL остановки системы проверки"""
        url = reverse('check_system:stop', args=[self.check_system.id])
        self.assertEqual(resolve(url).func, views.stop)
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка для гостя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_reject_list_url(self):
        """Тест URL списка обращений"""
        url = reverse('check_system:reject_list')
        self.assertEqual(resolve(url).func.view_class, views.RejectListView)
        
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_reject_detail_url(self):
        """Тест URL деталей обращения"""
        url = reverse('check_system:reject_detail', args=[self.reject.id])
        self.assertEqual(resolve(url).func.view_class, views.RejectDetailView)
        
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        """Тест доступа неавторизованных пользователей"""

        urls = [
            reverse('check_system:show_all'),
            reverse('check_system:show', args=[self.check_system.id]),
            reverse('check_system:show_all_reports', args=[self.check_system.id]),
            reverse('check_system:show_report', args=[self.report.id]),
            reverse('check_system:activate', args=[self.order.id]),
            reverse('check_system:load_report', args=[self.check_system.id]),
            reverse('check_system:stop', args=[self.check_system.id]),
            reverse('check_system:reject_list'),
            reverse('check_system:reject_detail', args=[self.reject.id])
        ]

        for url in urls:
            # Проверка для неавторизованного пользователя
            response = self.guest_client.get(url)
            self.assertIn(response.status_code, [302, 404])  # 302 - редирект на логин, 404 - страница не найдена
            if response.status_code == 302:
                self.assertRedirects(response, f'/users/login/?next={url}')

            # Проверка для пользователя без прав доступа
            response = self.other_client.get(url)
            self.assertIn(response.status_code, [403, 404])  # 403 - доступ запрещен, 404 - страница не найдена

    def tearDown(self):
        """Очистка данных после тестов"""
        Report.objects.all().delete()
        Reject.objects.all().delete()
        PetsitterCheck.objects.all().delete()
        Order.objects.all().delete()
        Category.objects.all().delete()
        Breed.objects.all().delete()
        User.objects.all().delete() 