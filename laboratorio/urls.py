from django.urls import path
from .views import terminal_views, chatbot_views

app_name = 'laboratorio'

urlpatterns = [
    path('api/terminal/', terminal_views.api_terminal, name='api_terminal'),
    path('api/seed-rapido/', terminal_views.api_seed_rapido, name='api_seed_rapido'),
    path('api/chatbot/', chatbot_views.api_chatbot, name='api_chatbot'),
]
