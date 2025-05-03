from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceRequest, Bid, Review, Message, Notification

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_resident', 'is_service_provider', 'rating')
    list_filter = ('is_resident', 'is_service_provider')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Kişisel Bilgiler', {'fields': ('first_name', 'last_name', 'email')}),
        ('Profil Bilgileri', {'fields': ('profile_picture', 'phone_number', 'address', 'bio', 'rating')}),
        ('İzinler', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_resident', 'is_service_provider')}),
        ('Önemli Tarihler', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'resident', 'service_type', 'urgency', 'status', 'created_at')
    list_filter = ('service_type', 'urgency', 'status')
    search_fields = ('title', 'description', 'resident__username')
    date_hierarchy = 'created_at'

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'service_provider', 'amount', 'is_accepted', 'created_at')
    list_filter = ('is_accepted',)
    search_fields = ('service_request__title', 'service_provider__username')
    date_hierarchy = 'created_at'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'reviewer', 'reviewed', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('service_request__title', 'reviewer__username', 'reviewed__username')
    date_hierarchy = 'created_at'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('sender__username', 'receiver__username', 'content')
    date_hierarchy = 'created_at'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'message')
    date_hierarchy = 'created_at'
