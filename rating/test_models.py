from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Review, ReviewImage, Reply
from django.utils import timezone

User = get_user_model()

class RatingModelsTest(TestCase):
    def setUp(self):
        """Создание начальных данных для тестов"""
        # Создаем тестовых пользователей
        self.reviewer = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='testpass123'
        )
        
        self.reviewed_user = User.objects.create_user(
            username='reviewed',
            email='reviewed@example.com',
            password='testpass123'
        )

        # Создаем базовый отзыв для тестов
        self.review = Review.objects.create(
            score=5,
            text='Отличный специалист!',
            reviewer=self.reviewer,
            user=self.reviewed_user
        )

    def test_review_creation(self):
        """Тест создания отзыва"""
        self.assertEqual(self.review.score, 5)
        self.assertEqual(self.review.text, 'Отличный специалист!')
        self.assertEqual(self.review.reviewer, self.reviewer)
        self.assertEqual(self.review.user, self.reviewed_user)
        self.assertFalse(self.review.published)
        self.assertIsNotNone(self.review.timestamp)

    def test_review_str_method(self):
        """Тест строкового представления отзыва"""
        expected_str = f"Отзыв на {self.reviewed_user.username} от {self.reviewer.username} номер {self.review.id}"
        self.assertEqual(str(self.review), expected_str)

    def test_review_default_values(self):
        """Тест значений по умолчанию для отзыва"""
        review = Review.objects.create(
            score=4,
            reviewer=self.reviewer,
            user=self.reviewed_user
        )
        self.assertEqual(review.text, "Пользователь не оставил комментарий к своей оценке")
        self.assertFalse(review.published)
        self.assertIsNone(review.video.name)

    def test_review_image_creation(self):
        """Тест создания изображения к отзыву"""
        # Создаем тестовый файл изображения
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        review_image = ReviewImage.objects.create(
            review=self.review,
            image=image_file
        )
        
        self.assertEqual(review_image.review, self.review)
        self.assertIsNotNone(review_image.image)

    def test_review_image_str_method(self):
        """Тест строкового представления изображения отзыва"""
        review_image = ReviewImage.objects.create(
            review=self.review
        )
        expected_str = f"Картинка к отзыву номер {self.review.id}"
        self.assertEqual(str(review_image), expected_str)

    def test_reply_creation(self):
        """Тест создания ответа на отзыв"""
        reply = Reply.objects.create(
            review=self.review,
            text='Спасибо за отзыв!'
        )
        
        self.assertEqual(reply.review, self.review)
        self.assertEqual(reply.text, 'Спасибо за отзыв!')
        self.assertIsNotNone(reply.timestamp)

    def test_reply_str_method(self):
        """Тест строкового представления ответа"""
        reply = Reply.objects.create(
            review=self.review,
            text='Спасибо за отзыв!'
        )
        expected_str = f"Ответ на отзыв от {self.reviewed_user.username} номер {reply.id}"
        self.assertEqual(str(reply), expected_str)

    def test_cascade_delete_review(self):
        """Тест каскадного удаления связанных объектов при удалении отзыва"""
        # Создаем связанные объекты
        review_image = ReviewImage.objects.create(review=self.review)
        reply = Reply.objects.create(review=self.review, text='Ответ')
        
        # Сохраняем ID для проверки
        review_id = self.review.id
        image_id = review_image.id
        reply_id = reply.id
        
        # Удаляем отзыв
        self.review.delete()
        
        # Проверяем что все связанные объекты удалены
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(id=review_id)
        with self.assertRaises(ReviewImage.DoesNotExist):
            ReviewImage.objects.get(id=image_id)
        with self.assertRaises(Reply.DoesNotExist):
            Reply.objects.get(id=reply_id)

    def test_review_score_validation(self):
        """Тест валидации оценки отзыва"""
        review = Review.objects.create(
            score=5,
            reviewer=self.reviewer,
            user=self.reviewed_user
        )
        self.assertTrue(0 <= review.score <= 5)

    def tearDown(self):
        """Очистка данных после тестов"""
        Review.objects.all().delete()
        ReviewImage.objects.all().delete()
        Reply.objects.all().delete()
        User.objects.all().delete() 