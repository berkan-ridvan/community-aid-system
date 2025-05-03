from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('service-request/create/', views.create_service_request, name='create_service_request'),
    path('service-request/<int:pk>/', views.service_request_detail, name='service_request_detail'),
    path('service-request/<int:pk>/complete/', views.complete_service, name='complete_service'),
    path('bid/<int:bid_id>/accept/', views.accept_bid, name='accept_bid'),
    path('search/', views.search_requests, name='search_requests'),
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:user_id>/', views.messages_list, name='messages_list'),
    path('chat/<int:user_id>/', views.chat, name='chat'),
    path('notifications/', views.notifications, name='notifications'),
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
] 