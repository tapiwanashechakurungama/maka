# Frontend-Backend Integration Guide

This guide ensures complete integration between the React Native frontend and Django backend.

## 🔗 API Endpoints Mapping

### Authentication Endpoints
| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|--------|-------------|
| `API_ENDPOINTS.REGISTER` | `/api/auth/register/` | POST | User registration |
| `API_ENDPOINTS.LOGIN` | `/api/auth/login/` | POST | User authentication |

### Booking Endpoints
| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|--------|-------------|
| `API_ENDPOINTS.CREATE_BOOKING` | `/api/bookings/create/` | POST | Create new booking |
| `API_ENDPOINTS.USER_BOOKINGS` | `/api/bookings/user/` | GET | Get user's bookings |
| `API_ENDPOINTS.CANCEL_BOOKING(id)` | `/api/bookings/{id}/cancel/` | PUT | Cancel booking |

### Notification Endpoints
| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|--------|-------------|
| `API_ENDPOINTS.NOTIFICATIONS` | `/api/notifications/` | GET | Get user notifications |
| `API_ENDPOINTS.MARK_NOTIFICATION_READ(id)` | `/api/notifications/{id}/read/` | PUT | Mark notification as read |
| `API_ENDPOINTS.MARK_ALL_READ` | `/api/notifications/mark-all-read/` | PUT | Mark all notifications as read |
| `API_ENDPOINTS.DELETE_NOTIFICATION(id)` | `/api/notifications/{id}/` | DELETE | Delete notification |
| `API_ENDPOINTS.UNREAD_COUNT` | `/api/notifications/unread-count/` | GET | Get unread count |

### Health Check
| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|--------|-------------|
| `API_ENDPOINTS.HEALTH` | `/api/health/` | GET | Health check |

## 📱 Data Format Compatibility

### Registration Request (Frontend → Backend)
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

### Registration Response (Backend → Frontend)
```json
{
  "id": 1,
  "username": "john@example.com",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "",
  "student_id": ""
}
```

### Login Request (Frontend → Backend)
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

### Login Response (Backend → Frontend)
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "john@example.com",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Booking Request (Frontend → Backend)
```json
{
  "from": "MSU Main Campus",
  "to": "City Center",
  "date": "2024-01-15",
  "time": "09:00 AM",
  "numberOfPassengers": 2,
  "phoneNumber": "1234567890"
}
```

### Booking Response (Backend → Frontend)
```json
{
  "booking_id": "550e8400-e29b-41d4-a716-446655440000",
  "user": 1,
  "route": 1,
  "bus": 1,
  "departure_date": "2024-01-15",
  "departure_time": "09:00:00",
  "number_of_passengers": 2,
  "phone_number": "1234567890",
  "total_price": "10.00",
  "status": "pending",
  "created_at": "2024-01-15T09:00:00Z"
}
```

### User Bookings Response (Backend → Frontend)
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "booking_id": "550e8400-e29b-41d4-a716-446655440000",
      "route_details": {
        "id": 1,
        "name": "MSU Main Campus to City Center",
        "from_station_name": "MSU Main Campus",
        "to_station_name": "City Center",
        "distance": 10.0,
        "estimated_duration": 30,
        "price": 5.0
      },
      "bus_details": {
        "id": 1,
        "bus_number": "BUS001",
        "license_plate": "ABC123",
        "capacity": 20,
        "driver_name": "Default Driver",
        "driver_phone": "1234567890",
        "status": "active"
      },
      "departure_date": "2024-01-15",
      "departure_time": "09:00:00",
      "number_of_passengers": 2,
      "phone_number": "1234567890",
      "total_price": "10.00",
      "status": "pending",
      "created_at": "2024-01-15T09:00:00Z"
    }
  ]
}
```

### Notifications Response (Backend → Frontend)
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Booking Confirmed",
      "message": "Your booking from MSU Main Campus to City Center has been confirmed.",
      "notification_type": "booking_confirmed",
      "is_read": false,
      "created_at": "2024-01-15T09:00:00Z"
    }
  ]
}
```

### Unread Count Response (Backend → Frontend)
```json
{
  "unreadCount": 1
}
```

## 🔐 Authentication Flow

### 1. Registration Flow
1. User fills registration form in mobile app
2. Mobile app sends `POST /api/auth/register/` with user data
3. Django creates user and returns user object
4. Mobile app shows success message and redirects to login

### 2. Login Flow
1. User enters email and password in mobile app
2. Mobile app sends `POST /api/auth/login/` with credentials
3. Django validates credentials and returns JWT token
4. Mobile app stores token in AsyncStorage
5. Mobile app uses token for authenticated requests

### 3. Authenticated Requests
1. Mobile app includes `Authorization: Bearer <token>` header
2. Django validates JWT token
3. If valid, Django processes request
4. If invalid, Django returns 401 Unauthorized

## 🧪 Testing Integration

### Run Integration Tests
```bash
cd backend
python test_frontend_integration.py
```

### Test Individual Components
```bash
# Test authentication
python test_auth.py

# Test end-to-end flow
python test_end_to_end.py

# Test API endpoints
python test_api.py
```

## 🚨 Common Issues & Solutions

### 1. CORS Issues
**Problem**: Frontend can't connect to backend
**Solution**: Ensure CORS is configured in `settings.py`
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:19006",  # Expo development server
]
```

### 2. JWT Token Issues
**Problem**: Token not being sent or accepted
**Solution**: Check token format and headers
```javascript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### 3. Data Format Mismatch
**Problem**: Frontend sends different format than backend expects
**Solution**: Update serializers to handle mobile app format
```python
# In UserSerializer
firstName = serializers.CharField(source='first_name', required=False)
lastName = serializers.CharField(source='last_name', required=False)
```

### 4. Network Connectivity
**Problem**: Mobile app can't reach backend
**Solution**: 
- Ensure Django server is running on correct port
- Check if using correct IP address (not localhost for mobile)
- Verify firewall settings

## 📊 Monitoring Integration

### Backend Logs
```bash
python manage.py runserver --verbosity=2
```

### Frontend Debug
```javascript
// Add to API calls for debugging
console.log('API Request:', { url, data, headers });
console.log('API Response:', response.data);
```

### Health Check
```bash
curl http://localhost:8000/api/health/
```

## ✅ Integration Checklist

- [ ] **Authentication**
  - [ ] Registration works with mobile app format
  - [ ] Login returns JWT token
  - [ ] Token is stored in AsyncStorage
  - [ ] Token is sent with authenticated requests

- [ ] **Booking System**
  - [ ] Create booking with mobile app data format
  - [ ] Fetch user bookings
  - [ ] Cancel booking
  - [ ] Booking notifications are created

- [ ] **Notifications**
  - [ ] Fetch user notifications
  - [ ] Mark notification as read
  - [ ] Mark all notifications as read
  - [ ] Delete notification
  - [ ] Get unread count

- [ ] **Error Handling**
  - [ ] Network errors are handled
  - [ ] Authentication errors are handled
  - [ ] Validation errors are displayed
  - [ ] Loading states are shown

- [ ] **Data Consistency**
  - [ ] Frontend data format matches backend expectations
  - [ ] Backend responses match frontend expectations
  - [ ] All required fields are present
  - [ ] Optional fields are handled properly

## 🚀 Production Considerations

### 1. Environment Variables
```bash
# Backend
export DEBUG=False
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url

# Frontend
export API_BASE_URL=https://your-api-domain.com/api
```

### 2. HTTPS
- Use HTTPS in production
- Update mobile app API base URL
- Configure SSL certificates

### 3. Rate Limiting
- Implement rate limiting for API endpoints
- Monitor API usage
- Set up alerts for unusual activity

### 4. Monitoring
- Set up logging for API calls
- Monitor error rates
- Track user activity
- Set up health checks

## 📚 Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [React Native Networking](https://reactnative.dev/docs/network)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [CORS Configuration](https://django-cors-headers.readthedocs.io/) 