from rest_framework.serializers import ModelSerializer
from .models import Schedule
from rest_framework.serializers import ModelSerializer, ValidationError

class ContactSerializers(ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    def validate_contact(self, value):
        if not isinstance(value, dict):
            raise ValidationError("Contact must be a valid JSON object.")
        return value
