from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from pet.models import Category
from users.models import User, Petsitter, City, Region
from datetime import date

class UsersModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание региона и города
        cls.region = Region.objects.create(name="Test Region")
        cls.city = City.objects.create(
            name="Test City",
            region=cls.region
        )

        # Создание обычного пользователя
        cls.user = User.objects.create(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone="+79991234567",
            birth_date=date(1990, 1, 1),
            about="Test about",
            city=cls.city,
            region=cls.region
        )

        # Создание категории для петситтера
        cls.category = Category.objects.create(name="Dog")

        # Создание петситтера
        cls.petsitter_user = User.objects.create(
            username="petsitter",
            first_name="Pet",
            last_name="Sitter",
            email="petsitter@example.com",
            phone="+79997654321",
            birth_date=date(1995, 1, 1),
            about="Petsitter about",
            is_petsitter=True,
            city=cls.city,
            region=cls.region
        )
        
        cls.petsitter = Petsitter.objects.create(
            user=cls.petsitter_user,
            experience="Меньше 1 года",
            min_price=1000.00
        )
        cls.petsitter.categories.add(cls.category)

    def test_region_creation(self):
        """Тест создания региона"""
        self.assertEqual(self.region.name, "Test Region")
        self.assertEqual(str(self.region), "Test Region")

    def test_city_creation(self):
        """Тест создания города"""
        self.assertEqual(self.city.name, "Test City")
        self.assertEqual(self.city.region, self.region)
        self.assertEqual(str(self.city), "Test City")

    def test_user_creation(self):
        """Тест создания пользователя"""
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(str(self.user.phone), "+79991234567")
        self.assertEqual(self.user.birth_date, date(1990, 1, 1))
        self.assertEqual(self.user.about, "Test about")
        self.assertEqual(self.user.city, self.city)
        self.assertEqual(self.user.region, self.region)
        self.assertEqual(self.user.rating, 0.0)
        self.assertFalse(self.user.is_petsitter)

    def test_user_str_method(self):
        """Тест строкового представления пользователя"""
        expected_str = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(str(self.user), expected_str)

    def test_user_get_absolute_url(self):
        """Тест получения абсолютного URL пользователя"""
        expected_url = reverse('main:user_profile', kwargs={'username': self.user.username})
        self.assertEqual(self.user.get_absolute_url(), expected_url)

    def test_petsitter_creation(self):
        """Тест создания петситтера"""
        self.assertTrue(self.petsitter_user.is_petsitter)
        self.assertEqual(self.petsitter.user, self.petsitter_user)
        self.assertEqual(self.petsitter.experience, "Меньше 1 года")
        self.assertEqual(float(self.petsitter.min_price), 1000.00)
        self.assertTrue(self.petsitter.categories.filter(id=self.category.id).exists())

    def test_petsitter_str_method(self):
        """Тест строкового представления петситтера"""
        expected_str = f"Пэтситтер {self.petsitter_user.first_name} {self.petsitter_user.last_name}"
        self.assertEqual(str(self.petsitter), expected_str)

    def test_petsitter_get_absolute_url(self):
        """Тест получения абсолютного URL петситтера"""
        expected_url = reverse('main:user_profile', kwargs={'username': self.petsitter_user.username})
        self.assertEqual(self.petsitter.get_absolute_url(), expected_url)

    def test_user_photo_upload(self):
        """Тест загрузки фото пользователя"""
        photo = SimpleUploadedFile(
            "test_photo.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        self.user.photo = photo
        self.user.save()
        
        self.assertTrue(self.user.photo)
        self.assertIn("users", self.user.photo.path)

    def test_petsitter_experience_choices(self):
        """Тест выбора опыта работы петситтера"""
        valid_choices = [choice[0] for choice in self.petsitter.CHOICES]
        self.assertIn(self.petsitter.experience, valid_choices)

    def test_user_rating_update(self):
        """Тест обновления рейтинга пользователя"""
        new_rating = 4.5
        self.user.rating = new_rating
        self.user.save()
        
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.rating, new_rating)

    def test_cascade_delete(self):
        """Тест каскадного удаления"""
        petsitter_id = self.petsitter.id
        self.petsitter_user.delete()
        
        with self.assertRaises(Petsitter.DoesNotExist):
            Petsitter.objects.get(id=petsitter_id)

    def test_city_verbose_name_plural(self):
        """Тест множественного числа для модели City"""
        self.assertEqual(City._meta.verbose_name_plural, "cities")

    def tearDown(self):
        """Очистка данных после тестов"""
        Category.objects.all().delete()
        Petsitter.objects.all().delete()
        User.objects.all().delete()
        City.objects.all().delete()
        Region.objects.all().delete() 