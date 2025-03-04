from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rating.models import Review, ReviewImage, Reply
from rating.forms import ReviewForm, ReviewImageForm, ReplyForm

User = get_user_model()

class RatingViewsTest(TestCase):
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

    def test_create_review_get(self):
        """Тест GET-запроса создания отзыва"""
        url = reverse('rating:create_review', args=[self.other_user.id])
        response = self.auth_client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ReviewForm)
        self.assertIsInstance(response.context['image_form'], ReviewImageForm)

    def test_create_review_post(self):
        """Тест POST-запроса создания отзыва с изображением"""
        url = reverse('rating:create_review', args=[self.other_user.id])
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        data = {
            'score': 4,
            'text': 'Новый отзыв',
            'images': [image]
        }
        
        response = self.auth_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)
        
        new_review = Review.objects.latest('timestamp') 
        self.assertEqual(new_review.score, 4)
        self.assertEqual(new_review.text, 'Новый отзыв')
        self.assertEqual(new_review.reviewer, self.user)
        self.assertEqual(new_review.user, self.other_user)

    def test_update_review_get(self):
        """Тест GET-запроса обновления отзыва"""
        url = reverse('rating:update_view', args=[self.review.id])
        response = self.auth_client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ReviewForm)
        self.assertIsInstance(response.context['review_image_form'], ReviewImageForm)

    def test_update_review_post(self):
        """Тест POST-запроса обновления отзыва"""
        url = reverse('rating:update_view', args=[self.review.id])
        data = {
            'score': 3,
            'text': 'Обновленный отзыв'
        }
        
        response = self.auth_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        self.review.refresh_from_db()
        self.assertEqual(self.review.score, 3)
        self.assertEqual(self.review.text, 'Обновленный отзыв')

    def test_delete_review(self):
        """Тест удаления отзыва"""
        url = reverse('rating:delete_review', args=[self.review.id])
        response = self.auth_client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_create_reply_get(self):
        """Тест GET-запроса создания ответа на отзыв"""
        url = reverse('rating:create_reply', args=[self.review.id])
        response = self.other_client.get(url)  # Владелец отзыва создает ответ
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ReplyForm)

    def test_create_reply_post(self):
        """Тест POST-запроса создания ответа на отзыв"""
        # Публикуем отзыв перед созданием ответа
        self.review.published = True
        self.review.save()
        
        url = reverse('rating:create_reply', args=[self.review.id])
        data = {
            'text': 'Спасибо за отзыв!'
        }
        
        response = self.other_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reply.objects.count(), 1)

    def test_create_reply_duplicate(self):
        """Тест создания повторного ответа на отзыв"""
        Reply.objects.create(review=self.review, text='Первый ответ')
        
        url = reverse('rating:create_reply', args=[self.review.id])
        data = {
            'text': 'Второй ответ'
        }
        
        response = self.other_client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Reply.objects.count(), 1)

    def test_update_reply(self):
        """Тест обновления ответа"""
        reply = Reply.objects.create(review=self.review, text='Исходный ответ')
        url = reverse('rating:update_reply', args=[reply.id])
        
        data = {
            'text': 'Обновленный ответ'
        }
        
        response = self.other_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        reply.refresh_from_db()
        self.assertEqual(reply.text, 'Обновленный ответ')

    def test_delete_reply(self):
        """Тест удаления ответа"""
        reply = Reply.objects.create(review=self.review, text='Ответ на удаление')
        url = reverse('rating:delete_reply', args=[reply.id])
        
        response = self.other_client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reply.objects.count(), 0)

    def test_unauthorized_access(self):
        """Тест доступа неавторизованных пользователей"""
        urls = [
            reverse('rating:create_review', args=[self.other_user.id]),
            reverse('rating:update_view', args=[self.review.id]),
            reverse('rating:delete_review', args=[self.review.id]),
            reverse('rating:create_reply', args=[self.review.id])
        ]
        
        for url in urls:
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code, 302)

    def test_create_reply_unpublished_review(self):
        """Тест создания ответа на неопубликованный отзыв"""
        url = reverse('rating:create_reply', args=[self.review.id])
        data = {
            'text': 'Спасибо за отзыв!'
        }
        
        response = self.other_client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Reply.objects.count(), 0)

    def tearDown(self):
        """Очистка данных после тестов"""
        Reply.objects.all().delete()
        Review.objects.all().delete()
        ReviewImage.objects.all().delete()
        User.objects.all().delete()
