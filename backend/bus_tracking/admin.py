from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('student_id', 'phone_number', 'profile_picture', 'is_student', 'is_admin')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_student', 'is_admin']
    list_filter = ['is_student', 'is_admin', 'is_active']

@admin.register(BusStation)
class BusStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'license_plate', 'driver_name', 'capacity', 'status']
    list_filter = ['status']
    search_fields = ['bus_number', 'license_plate', 'driver_name']

@admin.register(BusTracker)
class BusTrackerAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'bus', 'is_active', 'last_ping']
    list_filter = ['is_active']
    search_fields = ['device_id', 'bus__bus_number']

@admin.register(BusLocation)
class BusLocationAdmin(admin.ModelAdmin):
    list_display = ['bus', 'latitude', 'longitude', 'speed', 'timestamp']
    list_filter = ['bus', 'timestamp']
    ordering = ['-timestamp']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'from_station', 'to_station', 'distance', 'price', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ['bus', 'route', 'departure_time', 'days_of_week', 'is_active']
    list_filter = ['days_of_week', 'is_active']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'route', 'bus', 'departure_date', 'status', 'total_price']
    list_filter = ['status', 'departure_date']
    search_fields = ['booking_id', 'user__username']
    readonly_fields = ['booking_id', 'total_price']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['title', 'user__username']