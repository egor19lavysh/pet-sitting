from django.test import TestCase
from .models import Category, Breed, Pet


class CategoryModelTest(TestCase):
    '''
    Класс для тестирования модели Category.
    '''

    def setUp(self):
        self.category = Category(
            name="Собака"
        )

    def test_str_representation(self):
        self.assertEqual(str(self.category), "Собака")

    def test_saving_and_retrieving_book(self):
        Category.objects.create(
            name="Собака"
        )

        Category.objects.create(
            name="Кошка"
        )

        saved_categories = Category.objects.all()
        self.assertEqual(saved_categories.count(), 2)

        first_saved_category = saved_categories[0]
        second_saved_category = saved_categories[1]
        self.assertEqual(first_saved_category.name, "Собака")
        self.assertEqual(second_saved_category.name, "Кошка")

        first_saved_category.delete()
        second_saved_category.delete()

        saved_categories = Category.objects.all()
        self.assertEqual(saved_categories.count(), 0)


class BreedModelTest(TestCase):
    '''
    Класс для тестирования модели Breed
    '''

    def setUp(self) -> None:
        Category.objects.create(name="Корова")
        if category := Category.objects.filter(name="Корова"):
            self.breed = Breed.objects.create(
                name="Буренка",
                category=category
            )
        else:
            raise

