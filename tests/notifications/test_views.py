from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from notifications.models import Notification
from notifications.views import create_notification

User = get_user_model()

class TestNotificationViews(TestCase):
    def setUp(self):
        """Настройка начальных данных для тестов"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_create_notification_without_object_id(self):
        """Тест создания уведомления без object_id"""
        create_notification(
            type='other',
            message='Тестовое уведомление',
            user_id=self.user.id
        )
        
        notification = Notification.objects.first()
        self.assertEqual(notification.type, 'other')
        self.assertEqual(notification.message, 'Тестовое уведомление')
        self.assertEqual(notification.user, self.user)
        self.assertIsNone(notification.object_id)
        self.assertFalse(notification.is_read)

    def test_create_notification_with_object_id(self):
        """Тест создания уведомления с object_id"""
        create_notification(
            type='order_created',
            message='Создан новый заказ',
            user_id=self.user.id,
            object_id=1
        )
        
        notification = Notification.objects.first()
        self.assertEqual(notification.type, 'order_created')
        self.assertEqual(notification.message, 'Создан новый заказ')
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.object_id, 1)

    def test_get_notifications_view(self):
        """Тест получения списка уведомлений"""
        # Создаем тестовые уведомления
        Notification.objects.create(
            type='other',
            message='Тест 1',
            user=self.user
        )
        Notification.objects.create(
            type='other',
            message='Тест 2',
            user=self.user
        )

        response = self.client.get(reverse('notifications:get_notifications'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['ns']), 2)
        self.assertTemplateUsed(response, 'notifications/notifications.html')

    def test_notifications_marked_as_read(self):
        """Тест что уведомления помечаются как прочитанные после просмотра"""
        # Создаем непрочитанное уведомление
        notification = Notification.objects.create(
            type='other',
            message='Тест',
            user=self.user,
            is_read=False
        )

        self.client.get(reverse('notifications:get_notifications'))
        
        # Проверяем что уведомление помечено как прочитанное
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_get_notifications_unauthorized(self):
        """Тест доступа к уведомлениям неавторизованным пользователем"""
        self.client.logout()
        response = self.client.get(reverse('notifications:get_notifications'))
        self.assertEqual(response.status_code, 404)

    def test_get_notifications_empty_list(self):
        """Тест получения пустого списка уведомлений"""
        response = self.client.get(reverse('notifications:get_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['ns']), 0)
