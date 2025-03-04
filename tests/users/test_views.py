from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import Petsitter, City, Region
from pet.models import Category
from datetime import date
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.tokens import account_activation_token

User = get_user_model()

class UsersViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание региона и города
        cls.region = Region.objects.create(name="Test Region")
        cls.city = City.objects.create(
            name="Test City",
            region=cls.region
        )

        # Создание обычного пользователя
        cls.user = User.objects.create_user(
            username="test_user",
            password="testpass123",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone="+79991234567",
            birth_date=date(1990, 1, 1),
            about="Test about",
            city=cls.city,
            region=cls.region
        )

        # Создание петситтера
        cls.petsitter_user = User.objects.create_user(
            username="petsitter",
            password="testpass456",
            is_petsitter=True,
            city=cls.city,
            region=cls.region
        )
        
        # Создание категории для петситтера
        cls.category = Category.objects.create(name="Dog")
        
        cls.petsitter = Petsitter.objects.create(
            user=cls.petsitter_user,
            experience="Меньше 1 года",
            min_price=1000.00
        )
        cls.petsitter.categories.add(cls.category)

        # Создание клиентов
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        
        cls.petsitter_client = Client()
        cls.petsitter_client.force_login(cls.petsitter_user)
        
        cls.guest_client = Client()

    def test_login_view(self):
        """Тест представления входа"""
        url = reverse('users:login')
        
        # GET запрос
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # POST запрос с правильными данными
        data = {
            'login': 'test_user',
            'password': 'testpass123'
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

        # POST запрос с неправильными данными
        data = {
            'login': 'wrong_user',
            'password': 'wrong_pass'
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """Тест представления выхода"""
        url = reverse('users:logout')
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

    def test_register_user_view(self):
        """Тест представления регистрации пользователя"""
        url = reverse('users:register_user')
        
        # GET запрос
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # POST запрос с валидными данными
        data = {
            'username': 'new_user',
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '+79991234567',
            'birth_date': date(1991, 2, 1),
            'about': 'New user',
            'city': self.city.id,
            'region': self.region.id
        }
        
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        # Проверяем сообщение о необходимости подтверждения email
        #self.assertIn('Пожалуйста, подтвердите свой email', response.content.decode())

    def test_user_activation(self):
        """Тест активации пользователя"""
        # Создаем неактивного пользователя
        user = User.objects.create_user(
            username='new_user',
            password='newpass123',
            email='new@example.com',
            is_active=False
        )
        
        # Генерируем токен
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        
        # Вызываем представление активации
        url = reverse('users:activate', args=[uid, token])
        response = self.guest_client.get(url)
        
        # Проверяем что пользователь активирован
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Спасибо за подтверждение', response.content.decode())


    def test_register_petsitter_view(self):
        """Тест представления регистрации петситтера"""
        url = reverse('users:register_petsitter')
        
        # GET запрос
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # POST запрос с валидными данными
        data = {
            'experience': 'Меньше 1 года',
            'min_price': 1000.00,
            'categories': [self.category.id]
        }
        response = self.auth_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        
        # Проверяем что пользователь стал петситтером
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_petsitter)

    def test_user_update_view(self):
        """Тест представления обновления профиля пользователя"""
        url = reverse('users:update_user')
        
        # GET запрос
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # POST запрос с валидными данными
        data = {
            'username': 'updated_user',
            'first_name': 'Updated',
            'last_name': 'User',
            'phone': '+79991234567',
            'birth_date': '1990-01-01',
            'about': 'Updated about',
            'city': self.city.id,
            'region': self.region.id
        }
        response = self.auth_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        # Проверяем обновление данных
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_user')

    def test_petsitter_update_view(self):
        """Тест представления обновления профиля петситтера"""
        url = reverse('users:update_petsitter')
        
        # GET запрос от петситтера
        response = self.petsitter_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # POST запрос с валидными данными
        data = {
            'experience': 'От 1 до 3 лет',
            'min_price': 2000.00,
            'categories': [self.category.id]
        }
        response = self.petsitter_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        # Проверяем обновление данных
        self.petsitter.refresh_from_db()
        self.assertEqual(self.petsitter.experience, 'От 1 до 3 лет')
        self.assertEqual(float(self.petsitter.min_price), 2000.00)

    def test_user_delete_view(self):
        """Тест представления удаления пользователя"""
        url = reverse('users:delete_user')
        
        # GET запрос
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # POST запрос
        response = self.auth_client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        
        # Проверяем удаление пользователя
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_petsitter_delete_view(self):
        """Тест представления удаления профиля петситтера"""
        url = reverse('users:delete_petsitter')
        
        # GET запрос от петситтера
        response = self.petsitter_client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # GET запрос от обычного пользователя
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # POST запрос от петситтера
        response = self.petsitter_client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('main:index'))
        
        # Проверяем удаление записи петситтера
        # Получаем пользователя напрямую из базы, игнорируя кэш
        user = User.objects.get(username="petsitter")
        self.assertFalse(user.is_petsitter)
        self.assertEqual(Petsitter.objects.count(), 0)

    def tearDown(self):
        """Очистка данных после тестов"""
        Category.objects.all().delete()
        Petsitter.objects.all().delete()
        User.objects.all().delete()
        City.objects.all().delete()
        Region.objects.all().delete() 