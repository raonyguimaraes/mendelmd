from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chat_index'),
    path('new/', views.new_conversation, name='chat_new'),
    path('<int:conversation_id>/', views.conversation, name='chat_conversation'),
    path('<int:conversation_id>/send/', views.send_message, name='chat_send'),
    path('<int:conversation_id>/poll/', views.poll_messages, name='chat_poll'),
]
