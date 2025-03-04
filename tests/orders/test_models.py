from django.test import TestCase
from orders.models import Order
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from pet.models import Category, Breed
from datetime import datetime, timedelta
from django.db.models import ProtectedError

User = get_user_model()


class OrderModelTest(TestCase):
    """
    Класс для тестирования модели Order
    """

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create(
            username="test_owner",
            password="password",
            first_name="Иван",
            last_name="Иванов"
        )

        cls.petsitter = User.objects.create(
            username="test_petsitter",
            password="password"
        )

        cls.category = Category.objects.create(name="Собака")
        cls.breed = Breed.objects.create(category=cls.category, name="Мопс")

        cls.order = Order.objects.create(
            name="Шарик",
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

    def test_photo(self):
        self.assertIsInstance(self.order.photo.url, str)
        self.assertEqual(self.order.photo, self.order._meta.get_field('photo').default)
        self.assertEqual(self.order._meta.get_field('photo').verbose_name, "Фотография питомца")
        self.assertEqual(self.order._meta.get_field('photo').upload_to, "pets/")

    def test_name(self):
        self.assertIsInstance(self.order.name, str)
        self.assertEqual(self.order._meta.get_field('name').max_length, 255)
        self.assertEqual(self.order._meta.get_field('name').verbose_name, "Имя питомца")

    def test_category(self):
        self.assertIsInstance(self.order.category, Category)
        self.assertEqual(self.order._meta.get_field('category').verbose_name, "Возраст питомца")

        with self.assertRaises(ProtectedError) as e:
            self.category.delete()

    def test_breed(self):
        self.assertIsInstance(self.order.breed, Breed)
        self.assertEqual(self.order._meta.get_field('breed').verbose_name, "Категория питомца")

        with self.assertRaises(ProtectedError) as e:
            self.breed.delete()

    def test_age(self):
        self.assertEqual(self.order._meta.get_field('age').max_digits, 3)
        self.assertEqual(self.order._meta.get_field('age').decimal_places, 1)
        self.assertEqual(self.order._meta.get_field('age').verbose_name, "Возраст питомца")
        self.assertIsInstance(self.order.age, float)

    def test_weight(self):
        self.assertEqual(self.order._meta.get_field('weight').max_digits, 5)
        self.assertEqual(self.order._meta.get_field('weight').decimal_places, 2)
        self.assertEqual(self.order._meta.get_field('weight').verbose_name, "Вес питомца")
        self.assertIsInstance(self.order.weight, float)

    def test_certificate(self):
        self.assertFalse(self.order._meta.get_field('certificate').default)
        self.assertEqual(self.order._meta.get_field('certificate').verbose_name, "Сертификат с прививками")
        self.assertIsInstance(self.order.certificate, bool)

    def test_info(self):
        self.assertEqual(self.order._meta.get_field('info').verbose_name, "Дополнительная информация о питомце")
        self.assertIsInstance(self.order.info, str)

    def test_walking(self):
        self.assertEqual(self.order._meta.get_field('walking').default, 3)
        self.assertEqual(self.order._meta.get_field('walking').verbose_name, "Количество необходимых выгулов")
        self.assertIsInstance(self.order.walking, int)

    def test_place(self):
        self.assertEqual(self.order._meta.get_field('place').max_length, 255)
        self.assertEqual(self.order._meta.get_field('place').default, Order.HomeChoices.PETSITTER_HOME)
        self.assertEqual(self.order._meta.get_field('place').verbose_name, "Место передержки")
        self.assertIsInstance(self.order.place, str)
        self.assertIsInstance(self.order.place, str)

    def test_first_day(self):
        self.assertEqual(self.order._meta.get_field('first_day').verbose_name, "Дата начала передержки")
        self.assertIsInstance(self.order.first_day, datetime)

    def test_last_day(self):
        self.assertEqual(self.order._meta.get_field('last_day').verbose_name, "Дата конца передержки")
        self.assertIsInstance(self.order.last_day, datetime)

    def test_price(self):
        self.assertEqual(self.order._meta.get_field('price').default, 0)
        self.assertEqual(self.order._meta.get_field('price').verbose_name, "Цена передержки руб./день")
        self.assertGreaterEqual(self.order.price, 0)
        self.assertIsInstance(self.order.price, float)

    def test_owner(self):
        self.assertIsInstance(self.order.owner, User)
        self.assertEqual(self.order._meta.get_field('owner').verbose_name, "Владелец питомца")

        self.owner.delete()
        self.assertEqual(Order.objects.count(), 0)

    def test_petsitter(self):
        self.assertIsInstance(self.order.petsitter, User)
        self.assertEqual(self.order._meta.get_field('petsitter').verbose_name, "Петситтер")

        self.petsitter.delete()
        self.assertEqual(Order.objects.count(), 0)

    def test_status(self):
        self.assertEqual(self.order._meta.get_field('status').max_length, 255)
        self.assertEqual(self.order._meta.get_field('status').verbose_name, "Статус объявления")
        self.assertEqual(self.order.status, Order.StatusChoices.IN_PROCESS)
        self.assertIsInstance(self.order.status, str)

    def test_created_at(self):
        self.assertEqual(self.order._meta.get_field('created_at').verbose_name, "Время создания")
        self.assertTrue(self.order._meta.get_field('created_at').auto_now_add)
        self.assertIsInstance(self.order.created_at, datetime)

    def test_updated_at(self):
        self.assertEqual(self.order._meta.get_field('updated_at').verbose_name, "Время обновления")
        self.assertTrue(self.order._meta.get_field('updated_at').auto_now)
        self.assertIsInstance(self.order.updated_at, datetime)

    def test_str(self):
        self.assertEqual(str(self.order), "Заявка на передержку питомца на 5 дня от Иван Иванов")

    def test_clean_valid_data(self):
        order = Order(
            name='Персик',
            category=self.category,
            breed=self.breed,
            age=2.5,
            weight=25.5,
            certificate=True,
            info='Очень дружелюбный пес',
            walking=3,
            place=Order.HomeChoices.PETSITTER_HOME,
            first_day=datetime.now().date(),
            last_day=datetime.now().date() + timedelta(days=7),
            price=1000,
            owner=self.owner,
            petsitter=self.petsitter,
            status=Order.StatusChoices.IN_PROCESS
        )

        try:
            order.clean()
        except ValidationError:
            self.fail(msg="Метод clean модели Order вызывает ошибку при валидных данных")

    def test_clean_invalid_data(self):
        order = Order(
            name='Персик',
            category=self.category,
            breed=self.breed,
            age=2.5,
            weight=25.5,
            certificate=True,
            info='Очень дружелюбный пес',
            walking=3,
            place=Order.HomeChoices.PETSITTER_HOME,
            first_day=datetime.now().date(),
            last_day=datetime.now().date() - timedelta(days=7),
            price=1000,
            owner=self.owner,
            petsitter=self.petsitter,
            status=Order.StatusChoices.IN_PROCESS
        )

        with self.assertRaises(ValidationError) as context:
            order.clean()
        self.assertEqual(str(context.exception), "['Неправильно выбраны даты']")

    def test_clean_invalid_price(self):
        order = Order(
            name='Персик',
            category=self.category,
            breed=self.breed,
            age=2.5,
            weight=25.5,
            certificate=True,
            info='Очень дружелюбный пес',
            walking=3,
            place=Order.HomeChoices.PETSITTER_HOME,
            first_day=datetime.now().date(),
            last_day=datetime.now().date() + timedelta(days=7),
            price=-1000,
            owner=self.owner,
            petsitter=self.petsitter,
            status=Order.StatusChoices.IN_PROCESS
        )

        with self.assertRaises(ValidationError) as context:
            order.clean()
        self.assertEqual(str(context.exception), "['Цена не может отрицательной']")

    def tearDown(self) -> None:
        Order.objects.all().delete()
        Breed.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
