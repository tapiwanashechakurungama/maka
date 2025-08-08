# MSU Bus Tracking System

A comprehensive bus tracking and booking system for Midlands State University (MSU) with a React Native mobile app and Django REST Framework backend.

## 🏗️ Architecture

### Frontend (React Native App)
- **Framework**: Expo Router with React Native
- **UI**: Modern design with Tailwind CSS styling
- **Navigation**: Tab-based navigation with 5 main screens
- **Authentication**: JWT-based with AsyncStorage persistence

### Backend (Django REST Framework)
- **Framework**: Django 5.2.5 with DRF
- **Database**: SQLite3 (development) / MySQL (production)
- **Authentication**: JWT with SimpleJWT
- **Features**: WebSocket support, Swagger documentation

## 📱 Mobile App Features

### Core Screens
1. **Home** - Interactive map with MSU campus location and route search
2. **Authentication** - Login/Register with JWT tokens
3. **Booking System** - Complete booking form with validation
4. **Booked Buses** - Booking management with status tracking
5. **User Management** - Profile and notifications

### Advanced Features
- **Real-time Notifications** - Badge system with blinking animations
- **GPS Tracking** - Bus location updates with geofencing
- **Status Management** - Booking statuses (pending, confirmed, completed, cancelled)
- **Offline Support** - AsyncStorage for session persistence
- **Animations** - Lottie animations for enhanced UX

## 🚀 Quick Start

### Backend Setup

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Start the server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd app
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm start
   ```

3. **Run on device/simulator**:
   ```bash
   npm run ios    # iOS
   npm run android # Android
   ```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User authentication

### Bus System
- `GET /api/stations/` - List bus stations
- `GET /api/routes/` - List bus routes
- `GET /api/buses/` - List available buses

### Bookings
- `POST /api/bookings/create/` - Create new booking
- `GET /api/bookings/user/` - Get user's bookings
- `GET /api/bookings/<uuid>/` - Get booking details
- `POST /api/bookings/<uuid>/cancel/` - Cancel booking

### GPS Tracking
- `POST /api/location/update/` - Update bus location
- `GET /api/buses/<id>/track/` - Track specific bus

### Notifications
- `GET /api/notifications/` - Get user notifications
- `PATCH /api/notifications/<id>/read/` - Mark notification as read
- `PUT /api/notifications/mark-all-read/` - Mark all notifications as read
- `DELETE /api/notifications/<id>/` - Delete notification
- `GET /api/notifications/unread-count/` - Get unread count

## 📊 Database Models

### Core Models
- **User** - Extended AbstractUser with student_id, phone_number, profile_picture
- **BusStation** - GPS coordinates for bus stops
- **Bus** - Bus details with capacity, driver info, status
- **BusTracker** - GPS device tracking
- **BusLocation** - Real-time location data with speed, heading, accuracy
- **Route** - Bus routes with distance, duration, pricing
- **BusSchedule** - Timetables with days of week
- **Booking** - Comprehensive booking system with UUID
- **Notification** - Advanced notification system with types

## 🔒 Security Features

### Authentication
- JWT token-based authentication
- Password hashing with Django's built-in hashers
- Token expiration and refresh
- Secure storage with AsyncStorage

### Data Protection
- Input validation and sanitization
- CORS configuration
- Error handling without sensitive data exposure
- HTTPS enforcement

## 🎨 UI/UX Features

### Design System
- **Color Scheme**: Blue primary (#2563eb) with modern grays
- **Typography**: Clean, readable fonts
- **Icons**: Ionicons and custom emojis
- **Animations**: Smooth transitions and micro-interactions

### User Experience
- **Onboarding**: 3-step welcome flow
- **Authentication**: Secure login/register with validation
- **Real-time Updates**: Live notifications and status changes
- **Offline Support**: Local storage for session persistence
- **Responsive Design**: Adapts to different screen sizes

## 📚 Documentation

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **Health Check**: `http://localhost:8000/api/health/`

## 🧪 Testing

Run the API test script:
```bash
cd backend
python test_api.py
```

## 🚀 Deployment

### Backend (Django)
1. Set up production database (MySQL/PostgreSQL)
2. Configure environment variables
3. Run migrations
4. Deploy to your preferred platform (Heroku, AWS, etc.)

### Frontend (React Native)
1. Build for production
2. Deploy to app stores (iOS/Android)

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For support, please contact the development team or create an issue in the repository. 