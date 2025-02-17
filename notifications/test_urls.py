from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse
from .views import get_notifications
from django.template.loader import render_to_string

class TestUrls(SimpleTestCase):
    """Тесты для проверки URLs приложения notifications"""

    def setUp(self):
        self.client = Client()

    def test_get_notifications_url_resolves(self):
        """Тест URL для получения уведомлений"""
        url = reverse('notifications:get_notifications')
        self.assertEqual(resolve(url).func, get_notifications)

    def test_get_notifications_url_name(self):
        """Тест правильности формирования URL по имени"""
        self.assertEqual(reverse('notifications:get_notifications'), '/notifications/')

    def test_notifications_template_used(self):
        """Тест использования правильного шаблона для страницы уведомлений"""
        response = self.client.get(reverse('notifications:get_notifications'))
        self.assertTemplateUsed(response, 'notifications/notifications.html')