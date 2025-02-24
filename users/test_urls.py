from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from users.models import Petsitter, City, Region
from . import views

User = get_user_model()

class UsersUrlsTest(TestCase):
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
        cls.petsitter = Petsitter.objects.create(
            user=cls.petsitter_user,
            experience="Меньше 1 года",
            min_price=1000.00
        )

        # Создание клиентов
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        
        cls.petsitter_client = Client()
        cls.petsitter_client.force_login(cls.petsitter_user)
        
        cls.guest_client = Client()

    def test_login_url(self):
        """Тест URL авторизации"""
        url = reverse('users:login')
        self.assertEqual(resolve(url).func, views.login_user)
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'users/login.html')

    def test_logout_url(self):
        """Тест URL выхода из системы"""
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, views.logout_user)
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_register_types_url(self):
        """Тест URL выбора типа регистрации"""
        url = reverse('users:register')
        self.assertEqual(resolve(url).func, views.register_types)
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'users/register_types.html')

    def test_register_user_url(self):
        """Тест URL регистрации пользователя"""
        url = reverse('users:register_user')
        self.assertEqual(resolve(url).func, views.register_user)
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'users/register_user.html')

    def test_register_petsitter_url(self):
        """Тест URL регистрации петситтера"""
        url = reverse('users:register_petsitter')
        self.assertEqual(resolve(url).func, views.register_petsitter)

        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)
        #self.assertTemplateUsed(response, 'users/register_petsitter.html')

    def test_update_user_url(self):
        """Тест URL обновления профиля пользователя"""
        url = reverse('users:update_user')
        self.assertEqual(resolve(url).func.view_class, views.UserUpdate)
        
        # Проверка для авторизованного пользователя
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'users/user_form.html')
        
        # Проверка для гостя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_user_url(self):
        """Тест URL удаления пользователя"""
        url = reverse('users:delete_user')
        self.assertEqual(resolve(url).func.view_class, views.UserDelete)
        
        # Проверка для авторизованного пользователя
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'users/user_confirm_delete.html')
        
        # Проверка для гостя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_update_petsitter_url(self):
        """Тест URL обновления профиля петситтера"""
        url = reverse('users:update_petsitter')
        self.assertEqual(resolve(url).func.view_class, views.PetsitterUpdate)
        
        # Проверка для петситтера
        response = self.petsitter_client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'users/petsitter_form.html')
        
        # Проверка для обычного пользователя
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_petsitter_url(self):
        """Тест URL удаления профиля петситтера"""
        url = reverse('users:delete_petsitter')
        self.assertEqual(resolve(url).func.view_class, views.PetsitterDelete)
        
        # Проверка для петситтера
        response = self.petsitter_client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'users/petsitter_confirm_delete.html')
        
        # Проверка для неавторизованного пользователя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)  # Редирект на страницу логина
        self.assertRedirects(response, f'/users/login/?next={url}')

    def test_password_reset_urls(self):
        """Тест URL сброса пароля"""
        urls = [
            'users:password_reset',
            'users:password_reset_done',
            'users:password_reset_complete'
        ]
        for url_name in urls:
            url = reverse(url_name)
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_activate_url(self):
        """Тест URL активации аккаунта"""
        url = reverse('users:activate', args=['test-uidb64', 'test-token'])
        self.assertEqual(resolve(url).func, views.activate)

    def tearDown(self):
        """Очистка данных после тестов"""
        Petsitter.objects.all().delete()
        User.objects.all().delete()
        City.objects.all().delete()
        Region.objects.all().delete() 