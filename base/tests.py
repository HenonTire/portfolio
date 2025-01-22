from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Schedule
from .serilaizer import ContactSerializers

class ScheduleModelTest(TestCase):
    def test_create_schedule(self):
        schedule = Schedule.objects.create(
            name="John Doe",
            contact={"email": "john@example.com", "phone": "123456789"},
            message="This is a test message."
        )
        self.assertEqual(schedule.name, "John Doe")
        self.assertEqual(schedule.contact["email"], "john@example.com")
        self.assertEqual(schedule.message, "This is a test message.")
        self.assertEqual(str(schedule), "John Doe - This is a test message")

class ContactSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            "name": "Jane Doe",
            "contact": {"email": "jane@example.com", "phone": "987654321"},
            "message": "Hello, this is a test."
        }
        serializer = ContactSerializers(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Jane Doe")

    def test_invalid_data(self):
        data = {
            "name": "John Doe",
            "contact": "Not a JSON",  # Invalid JSON field
            "message": "Test message."
        }
        serializer = ContactSerializers(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("contact", serializer.errors)

class ContactViewTest(APITestCase):
    def test_contact_post_valid(self):
        data = {
            "name": "Alice",
            "contact": {"email": "alice@example.com", "phone": "111111111"},
            "message": "Test message from Alice."
        }
        response = self.client.post('/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "send message successfully!")
        self.assertEqual(Schedule.objects.count(), 1)
    
    def test_contact_post_invalid(self):
        data = {
            "name": "Bob",
            "contact": "Invalid JSON",  # Invalid JSON field
            "message": "Test message."
        }
        response = self.client.post('/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_list_schedules_as_admin(self):
        # Create a dummy schedule
        Schedule.objects.create(
            name="Charlie",
            contact={"email": "charlie@example.com", "phone": "222222222"},
            message="Test message from Charlie."
        )

        # Simulate an admin user
        self.client.force_authenticate(user=None, token="admin-token")  # Replace with actual admin auth if needed

        response = self.client.get('/list_schedules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Charlie")

    def test_list_schedules_as_non_admin(self):
        response = self.client.get('/list_schedules/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
