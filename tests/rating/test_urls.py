from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from rating.models import Review, Reply
from rating import views

User = get_user_model()

class RatingUrlsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание пользователей для тестов
        cls.user = User.objects.create(
            username="test_user",
            password="test123",
            first_name="Test",
            last_name="User"
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        cls.other_user = User.objects.create(
            username="other_user",
            password="test456",
            first_name="Other",
            last_name="User"
        )
        cls.other_client = Client()
        cls.other_client.force_login(cls.other_user)

        cls.guest_client = Client()

        # Создание тестового отзыва
        cls.review = Review.objects.create(
            score=5,
            text="Отличный специалист!",
            reviewer=cls.user,
            user=cls.other_user
        )

        # Создание тестового ответа
        cls.reply = Reply.objects.create(
            review=cls.review,
            text="Спасибо за отзыв!"
        )

    def test_create_review_url(self):
        """Тест URL создания отзыва"""
        url = reverse('rating:create_review', args=[self.other_user.id])
        self.assertEqual(resolve(url).func.view_class, views.ReviewCreateView)

        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_update_review_url(self):
        """Тест URL обновления отзыва"""
        url = reverse('rating:update_view', args=[self.review.id])
        self.assertEqual(resolve(url).func, views.review_update_view)

        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверка доступа другого пользователя
        response = self.other_client.get(url)
        self.assertEqual(response.status_code, 403)

        # Проверка доступа гостя
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_review_url(self):
        """Тест URL удаления отзыва"""
        url = reverse('rating:delete_review', args=[self.review.id])
        self.assertEqual(resolve(url).func.view_class, views.ReviewDeleteView)

        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)


        response = self.other_client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_create_reply_url(self):
        """Тест URL создания ответа на отзыв"""
        url = reverse('rating:create_reply', args=[self.review.id])
        self.assertEqual(resolve(url).func.view_class, views.ReplyCreateView)

        response = self.other_client.get(url)  # Владелец отзыва может ответить
        self.assertEqual(response.status_code, 200)

        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_update_reply_url(self):
        """Тест URL обновления ответа"""
        url = reverse('rating:update_reply', args=[self.reply.id])
        self.assertEqual(resolve(url).func.view_class, views.ReplyUpdateView)

        response = self.other_client.get(url)  # Владелец ответа
        self.assertEqual(response.status_code, 200)


        response = self.auth_client.get(url)  # Другой пользователь
        self.assertEqual(response.status_code, 403)

        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_reply_url(self):
        """Тест URL удаления ответа"""
        url = reverse('rating:delete_reply', args=[self.reply.id])
        self.assertEqual(resolve(url).func.view_class, views.ReplyDeleteView)

        response = self.other_client.get(url)  # Владелец ответа
        self.assertEqual(response.status_code, 200)


        response = self.auth_client.get(url)  # Другой пользователь
        self.assertEqual(response.status_code, 403)

        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        """Очистка данных после тестов"""
        Reply.objects.all().delete()
        Review.objects.all().delete()
        User.objects.all().delete()
