from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from notifications.models import Notification

User = get_user_model()

class NotificationModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.notification = Notification.objects.create(
            user=self.user,
            type='report_load',
            message='Тестовое уведомление',
            object_id=1
        )

    def test_notification_creation(self):
        """Тест создания уведомления"""
        self.assertEqual(self.notification.user.username, 'testuser')
        self.assertEqual(self.notification.type, 'report_load')
        self.assertEqual(self.notification.message, 'Тестовое уведомление')
        self.assertEqual(self.notification.object_id, 1)
        self.assertFalse(self.notification.is_read)
        self.assertIsNotNone(self.notification.timestamp)

    def test_notification_str_method(self):
        """Тест строкового представления уведомления"""
        expected_str = f"Уведомление для {self.user.username}"
        self.assertEqual(str(self.notification), expected_str)

    def test_notification_types(self):
        """Тест допустимых типов уведомлений"""
        valid_types = dict(Notification.Types)
        self.assertIn('report_load', valid_types)
        self.assertIn('report_watch', valid_types)
        self.assertIn('order_created', valid_types)
        self.assertIn('order_status', valid_types)
        self.assertIn('review', valid_types)
        self.assertIn('other', valid_types)

    def test_notification_mark_as_read(self):
        """Тест изменения статуса прочтения уведомления"""
        self.notification.is_read = True
        self.notification.save()
        updated_notification = Notification.objects.get(id=self.notification.id)
        self.assertTrue(updated_notification.is_read)

    def test_notification_cascade_delete(self):
        """Тест каскадного удаления уведомлений при удалении пользователя"""
        notification_id = self.notification.id
        self.user.delete()
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(id=notification_id)

    
    def tearDown(self) -> None:
        Notification.objects.all().delete()
        User.objects.all().delete()