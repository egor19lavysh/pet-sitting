from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from check_system.models import PetsitterCheck, Report, Reject, RejectImage
from orders.models import Order
from pet.models import Category, Breed
from datetime import date, datetime, timedelta

User = get_user_model()

class CheckSystemModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание пользователей
        cls.owner = User.objects.create_user(
            username='owner',
            password='testpass123',
            email='owner@example.com'
        )
        
        cls.petsitter = User.objects.create_user(
            username='petsitter',
            password='testpass123',
            email='petsitter@example.com',
            is_petsitter=True
        )

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
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5),
            start_time="12:00"
        )

    def test_petsitter_check_creation(self):
        """Тест создания системы проверки"""
        self.assertEqual(self.check_system.petsitter, self.petsitter)
        self.assertEqual(self.check_system.owner, self.owner)
        self.assertEqual(self.check_system.order, self.order)
        self.assertEqual(self.check_system.frequency, 3)
        self.assertEqual(self.check_system.interval, 4)
        self.assertEqual(self.check_system.status, "SUCCESS")
        self.assertEqual(self.check_system.rest, -1)

    def test_petsitter_check_str(self):
        """Тест строкового представления системы проверки"""
        expected_str = f"Система проверки для {self.petsitter} от {self.owner}"
        self.assertEqual(str(self.check_system), expected_str)

    def test_report_creation(self):
        """Тест создания отчета"""
        # Создаем тестовые файлы
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        video = SimpleUploadedFile(
            "test_video.mp4",
            b"file_content",
            content_type="video/mp4"
        )

        report = Report.objects.create(
            petsitter_check=self.check_system,
            text="Все хорошо, собака накормлена",
            image=image,
            video=video
        )

        self.assertEqual(report.petsitter_check, self.check_system)
        self.assertEqual(report.text, "Все хорошо, собака накормлена")
        self.assertTrue(report.image)
        self.assertTrue(report.video)
        self.assertIsNotNone(report.report_time)

    def test_report_validation(self):
        """Тест валидации отчета"""
        with self.assertRaises(ValidationError):
            Report.objects.create(
                petsitter_check=self.check_system,
                text=""  # Пустой текст
            )

    def test_reject_creation(self):
        """Тест создания обращения на остановку проверки"""
        video = SimpleUploadedFile(
            "reject_video.mp4",
            b"file_content",
            content_type="video/mp4"
        )

        reject = Reject.objects.create(
            system=self.check_system,
            text="Прошу остановить проверку",
            video=video
        )

        self.assertEqual(reject.system, self.check_system)
        self.assertEqual(reject.text, "Прошу остановить проверку")
        self.assertTrue(reject.video)
        self.assertEqual(reject.status, "В рассмотрении")
        self.assertIsNotNone(reject.timestamp)

    def test_reject_image_creation(self):
        """Тест создания изображения для обращения"""
        reject = Reject.objects.create(
            system=self.check_system,
            text="Прошу остановить проверку"
        )

        image = SimpleUploadedFile(
            "reject_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        reject_image = RejectImage.objects.create(
            reject=reject,
            image=image
        )

        self.assertEqual(reject_image.reject, reject)
        self.assertTrue(reject_image.image)

    def test_cascade_delete(self):
        """Тест каскадного удаления"""
        # Создаем связанные объекты
        report = Report.objects.create(
            petsitter_check=self.check_system,
            text="Тестовый отчет",
            image=SimpleUploadedFile("test.jpg", b"file_content"),
            video=SimpleUploadedFile("test.mp4", b"file_content")
        )

        reject = Reject.objects.create(
            system=self.check_system,
            text="Тестовое обращение"
        )

        # Сохраняем ID для проверки
        check_id = self.check_system.id
        report_id = report.id
        reject_id = reject.id

        # Удаляем систему проверки
        self.check_system.delete()

        # Проверяем что все связанные объекты удалены
        with self.assertRaises(PetsitterCheck.DoesNotExist):
            PetsitterCheck.objects.get(id=check_id)
        with self.assertRaises(Report.DoesNotExist):
            Report.objects.get(id=report_id)
        with self.assertRaises(Reject.DoesNotExist):
            Reject.objects.get(id=reject_id)

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