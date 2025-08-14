from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=False)
    firstName = serializers.CharField(source='first_name', required=False)
    lastName = serializers.CharField(source='last_name', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'student_id', 'phone_number', 'profile_picture', 'password', 'confirm_password',
                 'firstName', 'lastName')

    def validate(self, attrs):
        # Handle mobile app format (firstName, lastName)
        if 'firstName' in attrs:
            attrs['first_name'] = attrs.pop('firstName')
        if 'lastName' in attrs:
            attrs['last_name'] = attrs.pop('lastName')
        
        # Check password confirmation if provided
        if 'confirm_password' in attrs and attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Set confirm_password to password if not provided (for mobile app)
        if 'confirm_password' not in attrs:
            attrs['confirm_password'] = attrs['password']
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        # Generate username from email if not provided
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email']
        
        # Set default values for optional fields
        if not validated_data.get('phone_number'):
            validated_data['phone_number'] = ''
        if not validated_data.get('student_id'):
            validated_data['student_id'] = ''
            
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()  # Mobile app sends email
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate with email
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    if not user.is_active:
                        raise serializers.ValidationError('User account is disabled')
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('Invalid credentials')
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include email and password')

class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    current_location = serializers.SerializerMethodField()
    
    class Meta:
        model = Bus
        fields = '__all__'
    
    def get_current_location(self, obj):
        try:
            latest_location = obj.locations.latest()
            return {
                'latitude': str(latest_location.latitude),
                'longitude': str(latest_location.longitude),
                'timestamp': latest_location.timestamp,
                'speed': latest_location.speed
            }
        except BusLocation.DoesNotExist:
            return None

class BusTrackerSerializer(serializers.ModelSerializer):
    bus_number = serializers.CharField(source='bus.bus_number', read_only=True)
    
    class Meta:
        model = BusTracker
        fields = '__all__'

class BusLocationSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = BusLocation
        fields = ['device_id', 'latitude', 'longitude', 'altitude', 
                 'speed', 'heading', 'accuracy', 'satellites', 'timestamp']
    
    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        try:
            tracker = BusTracker.objects.get(device_id=device_id, is_active=True)
            validated_data['bus'] = tracker.bus
            
            # Update tracker last ping
            tracker.last_ping = timezone.now()
            tracker.save()
            
            # Create location record
            location = BusLocation.objects.create(**validated_data)
            
            # Trigger real-time updates (WebSocket)
            self.notify_location_update(location)
            
            return location
        except BusTracker.DoesNotExist:
            raise serializers.ValidationError("Invalid device ID or inactive tracker")
    
    def notify_location_update(self, location):
        # This would trigger WebSocket notifications
        pass

class RouteSerializer(serializers.ModelSerializer):
    from_station_name = serializers.CharField(source='from_station.name', read_only=True)
    to_station_name = serializers.CharField(source='to_station.name', read_only=True)
    
    class Meta:
        model = Route
        fields = '__all__'

class BusScheduleSerializer(serializers.ModelSerializer):
    bus_number = serializers.CharField(source='bus.bus_number', read_only=True)
    route_name = serializers.CharField(source='route.name', read_only=True)
    
    class Meta:
        model = BusSchedule
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    route_details = RouteSerializer(source='route', read_only=True)
    bus_details = BusSerializer(source='bus', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    

    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), write_only=True)
    bus = serializers.PrimaryKeyRelatedField(queryset=Bus.objects.all(), write_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('booking_id', 'user', 'total_price', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        from datetime import datetime
        route = validated_data.pop('route')  # This is now a Route instance
        bus = validated_data.pop('bus')      # This is now a Bus instance
        departure_date = validated_data.get('departure_date')
        departure_time = validated_data.get('departure_time')
        passengers = validated_data.get('number_of_passengers')
        phone = validated_data.get('phone_number')

        # If date/time are strings, parse them
        if isinstance(departure_date, str):
            departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
        if isinstance(departure_time, str):
            try:
                departure_time = datetime.strptime(departure_time, '%H:%M').time()
            except ValueError:
                departure_time = datetime.strptime(departure_time, '%H:%M:%S').time()

        # Calculate total price
        total_price = float(route.price) * passengers

        # Create booking
        booking = Booking.objects.create(
            user=self.context['request'].user,
            route=route,
            bus=bus,
            departure_date=departure_date,
            departure_time=departure_time,
            number_of_passengers=passengers,
            phone_number=phone,
            total_price=total_price,
            status='pending'
        )

        # Create confirmation notification
        Notification.objects.create(
            user=booking.user,
            title="Booking Confirmed",
            message=f"Your booking for route {route.name} has been confirmed.",
            notification_type='booking_confirmed',
            booking=booking
        )

        return booking

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at',)
