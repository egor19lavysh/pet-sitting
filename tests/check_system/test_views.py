from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from check_system.models import PetsitterCheck, Report, Reject, RejectImage
from orders.models import Order
from pet.models import Category, Breed
from datetime import datetime, timedelta

User = get_user_model()

class CheckSystemViewsTest(TestCase):
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

        # Создание тестовых файлов
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

        cls.guest_client = Client()

    def test_show_all_view(self):
        """Тест представления списка всех систем проверки"""
        url = reverse('check_system:show_all')
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('systems', response.context)
    

    def test_show_system_view(self):
        """Тест представления просмотра системы проверки"""
        url = reverse('check_system:show', args=[self.check_system.id])
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['system'], self.check_system)

    def test_show_all_reports_view(self):
        """Тест представления списка всех отчетов"""
        url = reverse('check_system:show_all_reports', args=[self.check_system.id])
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('reports', response.context)

    def test_show_report_view(self):
        """Тест представления просмотра отчета"""
        url = reverse('check_system:show_report', args=[self.report.id])
        
        # Проверка для владельца
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check_system/report.html')
        self.assertEqual(response.context['report'], self.report)

    def test_activate_view(self):
        """Тест представления активации системы проверки"""
        url = reverse('check_system:activate', args=[self.order.id])
        
        data = {
            'frequency': 4,
            'interval': 3,
            'start_time': '12:00'
        }
        
        # Проверка GET запроса
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка POST запроса
        response = self.owner_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        
        # Проверка создания системы
        new_system = PetsitterCheck.objects.latest('id')
        self.assertEqual(new_system.frequency, 4)
        self.assertEqual(new_system.interval, 3)
        self.assertEqual(str(new_system.start_time), '12:00:00')

    def test_load_report_view(self):
        """Тест представления загрузки отчета"""
        url = reverse('check_system:load_report', args=[self.check_system.id])
        
        data = {
            'petsitter_check': self.check_system.id,
            'text': 'Новый отчет',
            'image': SimpleUploadedFile("new_image.jpg", b"file_content", content_type="image/jpeg"),
            'video': SimpleUploadedFile("new_video.mp4", b"file_content", content_type="video/mp4")
        }
        
        # Проверка GET запроса
        response = self.petsitter_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка POST запроса
        response = self.petsitter_client.post(url, data)
        self.assertIn(response.status_code, [200, 302])  # Здесь может быть либо 200 (ошибка времени), либо 302 (успешный редирект)
        if response.status_code == 302:
            self.assertRedirects(response, reverse('main:index'))
        else:
            self.assertIn("Неподходящее время для отчета", response.content.decode())

    def test_stop_view(self):
        """Тест представления остановки системы проверки"""
        url = reverse('check_system:stop', args=[self.check_system.id])
        
        data = {
            'system': self.check_system.id,
            'text': 'Причина остановки',
            'video': SimpleUploadedFile("stop_video.mp4", b"file_content", content_type="video/mp4"),
            'images': [SimpleUploadedFile("stop_image.jpg", b"file_content", content_type="image/jpeg")]
        }
        
        # Проверка GET запроса
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Проверка POST запроса
        response = self.owner_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ваше обращение об остановке системы проверки сохранено', response.content.decode())

    def test_reject_list_view(self):
        """Тест представления списка обращений"""
        url = reverse('check_system:reject_list')
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_reject_detail_view(self):
        """Тест представления деталей обращения"""
        reject = Reject.objects.create(
            system=self.check_system,
            text="Тестовое обращение"
        )
        
        url = reverse('check_system:reject_detail', args=[reject.id])
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], reject)

    def tearDown(self):
        """Очистка данных после тестов"""
        Report.objects.all().delete()
        Reject.objects.all().delete()
        RejectImage.objects.all().delete()
        PetsitterCheck.objects.all().delete()
        Order.objects.all().delete()
        Category.objects.all().delete()
        Breed.objects.all().delete()
        User.objects.all().delete() 