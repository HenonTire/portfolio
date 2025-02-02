
from django.core.mail import send_mail 
from . models import Schedule
from django.conf import settings
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from .serilaizer import ContactSerializers
from rest_framework.response import Response


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def contact(request):
        
        serilaizer = ContactSerializers(data=request.data)

        if serilaizer.is_valid():
            name = serilaizer.validated_data['name']
            contact = serilaizer.validated_data['contact']
            message = serilaizer.validated_data['message']
        try:
            send_mail(
                    f"new contact form submission from {name}", 
                    f"it's {message}/n you can contact them by {contact} .",  
                    settings.EMAIL_HOST_USER,  
                    ['henontireso@gmail.com', 'fasil@gmail.com', ],  
                    fail_silently=False, 
                )
            meet = Schedule.objects.create(name=name, contact=contact, message=message)
            meet.save()
            return Response({'message': 'send message successfully!'}, status=200)
        except Exception as e:
                return Response({'error': str(e)}, status=400)
  
@api_view(['GET'])
@permission_classes([IsAdminUser])    
def list_schedules(request):
    schedules = Schedule.objects.all() 
    serializer = ContactSerializers(schedules, many=True)  
    return Response(serializer.data)


