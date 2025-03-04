from django.test import TestCase
from pet.models import Category, Breed, Pet
from django.contrib.auth import get_user_model


class CategoryModelTest(TestCase):
    """
    en: Class for testing model Category
    ru: Класс для тестирования модели Category
    """

    def setUp(self):
        self.category = Category.objects.create(name='Собака')

    def test_name_label(self):
        field_label = self.category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название категории животного')

    def test_name_max_length(self):
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_name(self):
        expected_object_name = self.category.name
        self.assertEqual(str(self.category), expected_object_name)

    def test_verbose_name_plural(self):
        verbose_name_plural = self.category._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'categories')

    @classmethod
    def tearDownClass(cls):
        Category.objects.all().delete()


class BreedModelTest(TestCase):
    '''
    en: Class for testing model Breed
    ru: Класс для тестирования модели Breed
    '''

    def setUp(self):
        category = Category.objects.create(name='Собака')
        self.breed = Breed.objects.create(
            category=category,
            name='Мопс'
        )

    def test_category_name(self):
        category_name = self.breed._meta.get_field('category').verbose_name
        self.assertEqual(category_name, "Категория животного")

    def test_breed_name(self):
        name = self.breed._meta.get_field('name').verbose_name
        self.assertEqual(name, "Название породы животного")

    def test_max_name_length(self):
        length = self.breed._meta.get_field('name').max_length
        self.assertEqual(length, 255)

    def test_str_repr(self):
        expected_name = self.breed.name
        self.assertEqual(str(self.breed), expected_name)

    @classmethod
    def tearDownClass(cls):
        Category.objects.all().delete()
        Breed.objects.all().delete()


class PetModelTest(TestCase):
    '''
    en: Class for testing model Pet
    ru: Класс для тестирования модели Pet
    '''

    def setUp(self):
        category = Category.objects.create(name='Собака')
        breed = Breed.objects.create(category=category, name='Лабрадор')
        user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.pet = Pet.objects.create(
            name='Кеня',
            age=2.5,
            category=category,
            breed=breed,
            owner=user,
            weight=25.5,
            certificate=True,
            info='Очень дружелюбный песик!'
        )

    def test_photo_url(self):
        expected_url = "/media/pets/default.jpg"
        self.assertEqual(self.pet.photo.url, expected_url)

    def test_verbose_name_photo(self):
        self.assertEqual(self.pet._meta.get_field("photo").verbose_name, "Фотография питомца")

    def test_verbose_name(self):
        self.assertEqual(self.pet._meta.get_field("name").verbose_name, "Имя питомца")

    def test_max_length_name(self):
        self.assertEqual(self.pet._meta.get_field("name").max_length, 255)

    def test_max_digits_age(self):
        self.assertEqual(self.pet._meta.get_field("age").max_digits, 4)

    def test_decimal_places_age(self):
        self.assertEqual(self.pet._meta.get_field("age").decimal_places, 1)

    def test_verbose_name_age(self):
        self.assertEqual(self.pet._meta.get_field("age").verbose_name, "Возраст питомца")

    def test_verbose_name_category(self):
        self.assertEqual(self.pet._meta.get_field("category").verbose_name, "Категория питомца")

    def test_verbose_name_breed(self):
        self.assertEqual(self.pet._meta.get_field("breed").verbose_name, "Порода питомца")

    def test_verbose_name_owner(self):
        self.assertEqual(self.pet._meta.get_field("owner").verbose_name, "Владелец Питомца")

    def test_verbose_name_weight(self):
        self.assertEqual(self.pet._meta.get_field("weight").verbose_name, "Вес питомца")

    def test_decimal_places_weight(self):
        self.assertEqual(self.pet._meta.get_field("weight").decimal_places, 2)

    def test_max_digits_weight(self):
        self.assertEqual(self.pet._meta.get_field("weight").max_digits, 5)

    def test_verbose_name_certificate(self):
        self.assertEqual(self.pet._meta.get_field("certificate").verbose_name, "Сертификат с прививками")

    def test_default_value_certificate(self):
        self.assertFalse(self.pet._meta.get_field("certificate").default)

    def test_verbose_name_info(self):
        self.assertEqual(self.pet._meta.get_field("info").verbose_name, "Дополнительная информация о питомце")

    @classmethod
    def tearDownClass(cls):
        Category.objects.all().delete()
        Breed.objects.all().delete()
        Pet.objects.all().delete()
