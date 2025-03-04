from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from pet.models import Pet, Category, Breed
from pet import views

User = get_user_model()


class PetUrlsTest(TestCase):
    def setUp(self):
        # Инициализация клиента для выполнения запросов
        self.guest_client = Client()  # Неавторизованный клиент

        # Авторизованный клиент
        self.user: User = User.objects.create(username="test_user", password="test123")
        self.auth_client = Client()
        self.auth_client.force_login(self.user)

        # Создание тестового питомца (экземпляра класс Pet)
        self.category = Category.objects.create(name="Собака")
        self.breed = Breed.objects.create(category=self.category, name="Мопс")
        self.pet = Pet.objects.create(
            name="Шарик",
            age=4.5,
            category=self.category,
            breed=self.breed,
            owner=self.user,
            weight=25.5,
            info="Добрый пес"
        )

    def test_create_pet_url(self):
        # Проверка, что URL 'create/' соответствует представлению create_pet
        url = reverse('pet:create_pet')
        self.assertEqual(resolve(url).func, views.create_pet)

        # Проверка, что страница возвращает статус 200 (OK)
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверка на неавторизованного пользователя
        self.assertEqual(self.guest_client.get(url).status_code, 302)

    def test_read_pet_url(self):
        # Проверка, что URL '<int:pk>/' соответствует представлению PetDetailView
        url = reverse('pet:read_pet', args=[self.pet.id])  # 1 — это пример pk
        self.assertEqual(resolve(url).func.view_class, views.PetDetailView)

        # Проверка, что страница возвращает статус 200 (OK)
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверка на неавторизованного пользователя
        self.assertEqual(self.guest_client.get(url).status_code, 302)

    def test_update_pet_url(self):
        # Проверка, что URL 'update/<int:pk>/' соответствует представлению update_pet
        url = reverse('pet:update_pet', args=[self.pet.id])  # 1 — это пример pk
        self.assertEqual(resolve(url).func, views.update_pet)

        # Проверка, что страница возвращает статус 200 (OK)
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверка на неавторизованного пользователя
        self.assertEqual(self.guest_client.get(url).status_code, 302)

    def test_delete_pet_url(self):
        # Проверка, что URL 'delete/<int:pk>/' соответствует представлению delete_pet
        url = reverse('pet:delete_pet', args=[self.pet.id])  # 1 — это пример pk
        self.assertEqual(resolve(url).func, views.delete_pet)

        # Проверка, что страница возвращает статус 200 (OK)
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверка на неавторизованного пользователя
        self.assertEqual(self.guest_client.get(url).status_code, 302)

    def test_save_pet_id_redirect_url(self):
        # Проверка, что URL 'create/order/<int:pk>/' соответствует представлению select_pet
        url = reverse('pet:save_pet_id', args=[self.pet.id])
        self.assertEqual(resolve(url).func, views.select_pet)

        # Проверка, что страница возвращает статус 200 (OK)
        response = self.auth_client.get(url)
        self.assertRedirects(response, "/petsitters/")

        # Проверка на неавторизованного пользователя
        self.assertEqual(self.guest_client.get(url).status_code, 302)

    def tearDown(self) -> None:
        Pet.objects.all().delete()
        Breed.objects.all().delete()
        Category.objects.all().delete()


