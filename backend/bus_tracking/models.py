from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class User(AbstractUser):
    """Extended User model for MSU Bus System"""
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_student = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class BusStation(models.Model):
    """Bus stations/stops model"""
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Bus(models.Model):
    """Bus model"""
    BUS_STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('inactive', 'Inactive'),
    ]

    bus_number = models.CharField(max_length=20, unique=True)
    license_plate = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=BUS_STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bus {self.bus_number} - {self.driver_name}"

    class Meta:
        ordering = ['bus_number']

class BusTracker(models.Model):
    """GPS Tracker for buses"""
    device_id = models.CharField(max_length=50, unique=True)
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE, related_name='tracker')
    is_active = models.BooleanField(default=True)
    last_ping = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tracker {self.device_id} - {self.bus.bus_number}"

class BusLocation(models.Model):
    """Real-time bus location data"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    altitude = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)  # km/h
    heading = models.FloatField(default=0.0)  # degrees
    accuracy = models.FloatField(default=0.0)  # meters
    satellites = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus.bus_number} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'

class Route(models.Model):
    """Bus routes"""
    name = models.CharField(max_length=100)
    from_station = models.ForeignKey(BusStation, on_delete=models.CASCADE, related_name='routes_from')
    to_station = models.ForeignKey(BusStation, on_delete=models.CASCADE, related_name='routes_to')
    distance = models.FloatField(help_text="Distance in kilometers")
    estimated_duration = models.PositiveIntegerField(help_text="Estimated duration in minutes")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_station.name} → {self.to_station.name}"

    class Meta:
        ordering = ['name']

class BusSchedule(models.Model):
    """Bus schedule/timetable"""
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='schedules')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    days_of_week = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus.bus_number} - {self.route} - {self.departure_time}"

    class Meta:
        ordering = ['departure_time']

class Booking(models.Model):
    """Bus booking model"""
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bookings')
    departure_date = models.DateField()
    departure_time = models.TimeField()
    number_of_passengers = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    phone_number = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    """User notifications"""
    NOTIFICATION_TYPES = [
        ('booking_confirmed', 'Booking Confirmed'),
        ('bus_approaching', 'Bus Approaching'),
        ('bus_delayed', 'Bus Delayed'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('system_update', 'System Update'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']
