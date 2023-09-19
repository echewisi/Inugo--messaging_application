# chat/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_message_read_status(request):
    try:
        message_id = request.data['message_id']
        message = Message.objects.get(id=message_id)

        # Check if the user is the recipient of the message
        if message.recipient != request.user:
            return Response({'detail': 'You do not have permission to mark this message as read.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the read_at field
        message.read_at = timezone.now()
        message.save()

        return Response({'detail': 'Message marked as read.'}, status=status.HTTP_200_OK)

    except Message.DoesNotExist:
        return Response({'detail': 'Message not found.'}, status=status.HTTP_404_NOT_FOUND)
