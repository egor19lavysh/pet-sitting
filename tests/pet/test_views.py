from django.http import HttpResponseForbidden
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
#from pet.views import select_pet
from pet.models import Category, Breed, Pet
from pet.forms import PetForm

User = get_user_model()


class ViewsTests(TestCase):
    """
    Класс для тестирования view-функций приложения pet
    """

    def setUp(self) -> None:
        """
        Инициализация клиента для выполнения запросов
        """

        self.guest_client = Client()  # Неавторизованный клиент

        # Авторизованный клиент
        self.user = User.objects.create(username="test_user", password="test123")
        self.other_user = User.objects.create(username="test_user2", password="test1232")
        self.auth_client = Client()
        self.other_client = Client()
        self.auth_client.force_login(self.user)
        self.other_client.force_login(self.other_user)

        # Создание категории животного и породы
        self.category = Category.objects.create(name="Собака")
        self.breed = Breed.objects.create(category=self.category, name="Собака")
        self.test_pet = Pet.objects.create(name="Шарик",
                                           age=2.5,
                                           category=self.category,
                                           breed=self.breed,
                                           owner=self.user,
                                           weight=15,
                                           info="smth"
                                           )

    # Тестирование функции create_pet
    def test_create_pet_get_request(self):
        """
        Проверка get-запроса к функции create_pet
        """
        response = self.auth_client.get(reverse("pet:create_pet"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], PetForm)

    def test_create_pet_post_request(self):
        """
        Проверка post-запроса к функции create_pet
        """
        response = self.auth_client.post(reverse("pet:create_pet"),
                                         data={
                                             "name": "Персик",
                                             "age": 2.5,
                                             "category": self.category.id,
                                             "breed": self.breed.id,
                                             "weight": 25.7,
                                             "info": "Прикольный собакен"
                                         })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pet.objects.count(), 2)
        self.assertEqual(Pet.objects.all()[1].owner, self.user)

    def test_create_pet_post_request_invalid_data(self):
        """
        Проверка post-запроса к функции create_pet с 'плохими' данными
        """
        response = self.auth_client.post(reverse("pet:create_pet"),
                                         data={
                                             "name": "Персик",
                                             "age": 2.5,
                                             "category": 10,
                                             "breed": "",
                                             "weight": "",
                                             "info": False
                                         })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], PetForm)

    def test_pet_detail_view_get_request(self):
        """
        Проверка get-запроса к CBF PetDetailView
        """
        response = self.auth_client.get(reverse("pet:read_pet", args=[self.test_pet.id]))
        self.assertEqual(response.status_code, 200)

    def test_pet_detail_view_other_owner(self):
        """
        Проверка get-запроса к CBF PetDetailView от клиента, который не является хозяином питомца
        """
        response = self.other_client.get(reverse("pet:read_pet", args=[self.test_pet.id]))
        self.assertIsInstance(response, HttpResponseForbidden)
        self.assertEqual(response.status_code, 403)

    def test_pet_detail_view_no_pet(self):
        """
        Проверка get-запроса к CBF PetDetailView с аргументом id, который не принадлежит ни одному питомцу
        """
        response = self.other_client.get(reverse("pet:read_pet", args=[3]))
        self.assertEqual(response.status_code, 404)

    # Тестирование функции update_pet
    def test_update_pet_no_pet(self):
        """
        Проверка get-запроса к функции update_pet с аргументом id, который не принадлежит ни одному питомцу
        """
        response = self.auth_client.get(reverse("pet:update_pet", args=[3]))
        self.assertEqual(response.status_code, 404)

    def test_update_pet_other_owner(self):
        """
        Проверка get-запроса к функции update_pet от клиента, который не является хозяином питомца
        """
        response = self.other_client.get(reverse("pet:update_pet", args=[self.test_pet.id]))
        self.assertIsInstance(response, HttpResponseForbidden)
        self.assertEqual(response.status_code, 403)

    def test_update_pet_get_request(self):
        """
        Проверка get-запроса к функции update_pet
        """
        response = self.auth_client.get(reverse("pet:update_pet", args=[self.test_pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], PetForm)

    def test_update_pet_post_request(self):
        """
        Проверка post-запроса к функции update_pet
        """
        response = self.auth_client.post(reverse("pet:update_pet", args=[self.test_pet.id]),
                                         data={
                                             "name": "Панч",
                                             "age": 3.5,
                                             "category": self.category.id,
                                             "breed": self.breed.id,
                                             "weight": 25.7,
                                             "info": "Очень cool собакен"
                                         })
        
        self.assertEqual(response.status_code, 302)
        self.test_pet.refresh_from_db()
        self.assertEqual(self.test_pet.name, "Панч")

    def test_update_pet_post_request_invalid_data(self):
        """
        Проверка post-запроса к функции update_pet от клиента с 'плохими' данными
        """
        response = self.auth_client.post(reverse("pet:update_pet", args=[self.test_pet.id]),
                                         data={
                                             "name": 10,
                                             "age": 3.5,
                                             "category": True,
                                             "breed": self.breed.id,
                                             "weight": 25.7,
                                             "info": "Очень cool собакен"
                                         })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], PetForm)

        self.test_pet.refresh_from_db()
        self.assertEqual(self.test_pet.name, "Шарик")
        self.assertEqual(self.test_pet.category, self.category)
        self.assertEqual(self.test_pet.info, "smth")

    # Тестирование функции select_pet
    # def test_select_pet_get_request(self):
    #     """
    #     Проверка post-запроса к функции select_pet от клиента
    #     """
    #     response = self.auth_client.get(reverse("pet:save_pet_id", args=[self.test_pet.id]))
    #     session = self.auth_client.session
    #     self.assertEqual(session["pet_id"], self.test_pet.id)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse("main:show_petsitters"))

    # def test_select_pet_other_owner(self):
    #     """
    #     Проверка get-запроса к функции select_pet от клиента, который не является хозяином питомца
    #     """
    #     response = self.other_client.get(reverse("pet:save_pet_id", args=[self.test_pet.id]))
    #     self.assertEqual(response.status_code, 403)
    #     self.assertIsInstance(response, HttpResponseForbidden)

    # def test_select_pet_no_pet(self):
    #     """
    #     Проверка get-запроса к функции select_pet с аргументом id, который не принадлежит ни одному питомцу
    #     """
    #     response = self.auth_client.get(reverse("pet:save_pet_id", args=[4]))
    #     self.assertEqual(response.status_code, 404)

    # Тестирование функции delete_pet
    def test_delete_pet_get_request(self):
        """
        Проверка get-запроса к функции delete_pet
        """
        response = self.auth_client.get(reverse("pet:delete_pet", args=[self.test_pet.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_pet_post_request(self):
        """
        Проверка post-запроса к функции delete_pet
        """
        response = self.auth_client.post(reverse("pet:delete_pet", args=[self.test_pet.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pet.objects.filter(name="Шарик").count(), 0)

    def test_delete_pet_other_owner(self):
        """
        Проверка post-запроса к функции delete_pet от клиента, который не является хозяином питомца
        """
        response = self.other_client.post(reverse("pet:delete_pet", args=[self.test_pet.id]))
        self.assertEqual(response.status_code, 403)
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_delete_pet_no_pet(self):
        """
        Проверка post-запроса к функции delete_pet с аргументом id, который не принадлежит ни одному питомцу
        """
        response = self.other_client.post(reverse("pet:delete_pet", args=[4]))
        self.assertEqual(response.status_code, 404)

    def tearDown(self) -> None:
        Pet.objects.all().delete()
        Breed.objects.all().delete()
        Category.objects.all().delete()