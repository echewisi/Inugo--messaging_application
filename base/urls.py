
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('api/mark-message-read/', views.update_message_read_status, name='update_message_read_status'),
]
