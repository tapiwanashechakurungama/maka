from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health'),
    
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    
    # Bus system
    path('stations/', views.BusStationListView.as_view(), name='stations'),
    path('stations/<int:pk>/', views.BusStationDetailView.as_view(), name='station-detail'),
    path('routes/', views.RouteListView.as_view(), name='routes'),
    path('schedules/', views.BusScheduleListView.as_view(), name='schedules'),
    path('schedules/<int:pk>/', views.BusScheduleDetailView.as_view(), name='schedule-detail'),
    path('buses/', views.BusListView.as_view(), name='buses'),
    path('buses/<int:pk>/', views.BusDetailView.as_view(), name='bus-detail'),
    
    # Bookings
    path('bookings/create/', views.BookingCreateView.as_view(), name='create-booking'),
    path('bookings/user/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('bookings/<uuid:booking_id>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<uuid:booking_id>/cancel/', views.cancel_booking, name='cancel-booking'),
    # Admin bookings
    path('admin/bookings/', views.AdminBookingListView.as_view(), name='admin-bookings'),
    path('admin/bookings/<int:pk>/', views.AdminBookingDetailView.as_view(), name='admin-booking-detail'),
    
    # GPS Tracking
    path('location/update/', views.BusLocationUpdateView.as_view(), name='location-update'),
    path('buses/<int:id>/track/', views.BusTrackingView.as_view(), name='track-bus'),
    
    # Users (admin)
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    path('notifications/<int:notification_id>/', views.delete_notification, name='delete-notification'),
    path('notifications/unread-count/', views.get_unread_count, name='unread-count'),

    # Analytics
    path('analytics/', views.analytics_summary, name='analytics-summary'),
]
