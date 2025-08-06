from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health'),
    
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    
    # Bus system
    path('stations/', views.BusStationListView.as_view(), name='stations'),
    path('routes/', views.RouteListView.as_view(), name='routes'),
    path('buses/', views.BusListView.as_view(), name='buses'),
    
    # Bookings
    path('bookings/create/', views.BookingCreateView.as_view(), name='create-booking'),
    path('bookings/user/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('bookings/<uuid:booking_id>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<uuid:booking_id>/cancel/', views.cancel_booking, name='cancel-booking'),
    
    # GPS Tracking
    path('location/update/', views.BusLocationUpdateView.as_view(), name='location-update'),
    path('buses/<int:id>/track/', views.BusTrackingView.as_view(), name='track-bus'),
    
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    path('notifications/<int:notification_id>/', views.delete_notification, name='delete-notification'),
    path('notifications/unread-count/', views.get_unread_count, name='unread-count'),
]
