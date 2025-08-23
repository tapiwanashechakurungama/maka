from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from .models import User, BusStation, Bus, BusLocation, Route, BusSchedule, Booking, Notification

from .serializers import (
    UserSerializer, LoginSerializer, BusStationSerializer, BusSerializer,
    BusLocationSerializer, RouteSerializer, BusScheduleSerializer,
    BookingSerializer, NotificationSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        'status': 'healthy',
        'message': 'MSU Bus Tracking System API is running',
        'timestamp': timezone.now()
    })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Return detailed error messages for debugging
            return Response({"error": serializer.errors}, status=400)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),  # Match mobile app expectation
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

class BusStationListView(generics.ListCreateAPIView):
    queryset = BusStation.objects.all()
    serializer_class = BusStationSerializer
    permission_classes = [AllowAny]

class BusStationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusStation.objects.all()
    serializer_class = BusStationSerializer
    permission_classes = [AllowAny]

class RouteListView(generics.ListAPIView):
    queryset = Route.objects.filter(is_active=True)
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]

class BusScheduleListView(generics.ListCreateAPIView):
    queryset = BusSchedule.objects.all()
    serializer_class = BusScheduleSerializer
    permission_classes = [AllowAny]

class BusScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusSchedule.objects.all()
    serializer_class = BusScheduleSerializer
    permission_classes = [AllowAny]

class BusListView(generics.ListAPIView):
    serializer_class = BusSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # By default, return all buses so published state persists visibly
        queryset = Bus.objects.all()
        status_param = self.request.query_params.get('status')
        if status_param and status_param.lower() in ['active', 'inactive', 'maintenance']:
            queryset = queryset.filter(status=status_param.lower())
        route_id = self.request.query_params.get('route_id')
        if route_id:
            # Filter buses available for specific route
            queryset = queryset.filter(schedules__route_id=route_id, schedules__is_active=True)
        return queryset

class BusDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = BusSerializer
    permission_classes = [AllowAny]
    queryset = Bus.objects.all()

# Allow POST to /api/buses/ for bus creation
class BusCreateView(generics.CreateAPIView):
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Bus.objects.all()

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Admin-oriented booking management (list all, update/delete)
class AdminBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    queryset = Booking.objects.all()

class AdminBookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    queryset = Booking.objects.all()

class BookingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'booking_id'
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        if booking.status in ['completed', 'cancelled']:
            return Response(
                {'error': 'Cannot cancel this booking'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        # Create cancellation notification
        Notification.objects.create(
            user=booking.user,
            title="Booking Cancelled",
            message=f"Your booking {booking.booking_id} has been cancelled.",
            notification_type='booking_cancelled',
            booking=booking
        )
        
        return Response({'message': 'Booking cancelled successfully'})
    except Booking.DoesNotExist:
        return Response(
            {'error': 'Booking not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

class BusLocationUpdateView(generics.CreateAPIView):
    serializer_class = BusLocationSerializer
    permission_classes = [AllowAny]  # GPS trackers don't authenticate
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = serializer.save()
        
        # Check for nearby bookings and send notifications
        self.check_bus_approaching_notifications(location)
        
        return Response({
            'status': 'success',
            'message': 'Location updated successfully',
            'bus': location.bus.bus_number
        }, status=status.HTTP_201_CREATED)
    
    def check_bus_approaching_notifications(self, location):
        # Find bookings for this bus today
        today = timezone.now().date()
        bookings = Booking.objects.filter(
            bus=location.bus,
            departure_date=today,
            status='confirmed'
        )
        
        # This is a simplified version - you'd implement proper geofencing
        for booking in bookings:
            # Check if bus is approaching (within 500m of pickup station)
            # You'd use proper distance calculation here
            Notification.objects.create(
                user=booking.user,
                title="Bus Approaching!",
                message=f"Bus {location.bus.bus_number} is approaching your pickup station.",
                notification_type='bus_approaching',
                booking=booking
            )

class BusTrackingView(generics.RetrieveAPIView):
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Bus.objects.filter(status='active')
    
    def retrieve(self, request, *args, **kwargs):
        bus = self.get_object()
        serializer = self.get_serializer(bus)
        
        # Get recent locations for tracking
        recent_locations = BusLocation.objects.filter(
            bus=bus,
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).order_by('-timestamp')[:10]
        
        location_data = [{
            'latitude': str(loc.latitude),
            'longitude': str(loc.longitude),
            'timestamp': loc.timestamp,
            'speed': loc.speed
        } for loc in recent_locations]
        
        response_data = serializer.data
        response_data['recent_locations'] = location_data
        
        return Response(response_data)

# --- Users ---
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        # Allow admins to access any user; non-admins only their own record
        if user.is_staff or user.is_superuser or obj.pk == user.pk:
            return obj
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("You do not have permission to access this user.")

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id, 
            user=request.user
        )
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    try:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})
    except Exception as e:
        return Response(
            {'error': 'Failed to mark notifications as read'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id, 
            user=request.user
        )
        notification.delete()
        return Response({'message': 'Notification deleted successfully'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_count(request):
    try:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unreadCount': unread_count})
    except Exception as e:
        return Response(
            {'error': 'Failed to get unread count'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# --- Analytics Endpoint ---
@api_view(['GET'])
@permission_classes([AllowAny])
def analytics_summary(request):
    """Return summary analytics used by the web dashboard.

    Response schema:
    {
      "bookings_today": int,
      "bookings_last_7_days": [{"day": "Mon", "count": 3}, ...],
      "route_demand": [{"name": "Route Name", "value": 10}, ...]
    }
    """
    try:
        today = timezone.now().date()

        # Count bookings today (exclude cancelled)
        bookings_today = Booking.objects.filter(
            departure_date=today
        ).exclude(status='cancelled').count()

        # Last 7 days booking counts by day label
        days = []
        for i in range(6, -1, -1):  # 6..0 => oldest to newest
            d = today - timedelta(days=i)
            count = Booking.objects.filter(departure_date=d).exclude(status='cancelled').count()
            days.append({
                'day': d.strftime('%a'),  # Mon, Tue, ...
                'count': count
            })

        # Route demand: total bookings per route (exclude cancelled)
        route_counts = (
            Booking.objects.exclude(status='cancelled')
            .values('route__name')
        )
        # Materialize counts per route name
        demand_map = {}
        for rc in route_counts:
            name = rc['route__name'] or 'Unknown Route'
            demand_map[name] = demand_map.get(name, 0) + 1
        route_demand = [
            {'name': name, 'value': value} for name, value in demand_map.items()
        ]

        data = {
            'bookings_today': bookings_today,
            'bookings_last_7_days': days,
            'route_demand': route_demand,
        }
        return Response(data)
    except Exception as e:
        return Response({'error': 'Failed to compute analytics'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)