# MSU Bus Tracking System - Django Backend

This is the Django REST Framework backend for the MSU Bus Tracking System.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- **Health Check**: `GET /api/health/`
- **Authentication**: 
  - `POST /api/auth/register/`
  - `POST /api/auth/login/`
- **Bus System**:
  - `GET /api/stations/`
  - `GET /api/routes/`
  - `GET /api/buses/`
- **Bookings**:
  - `POST /api/bookings/create/`
  - `GET /api/bookings/user/`
  - `GET /api/bookings/<uuid>/`
  - `POST /api/bookings/<uuid>/cancel/`
- **GPS Tracking**:
  - `POST /api/location/update/`
  - `GET /api/buses/<id>/track/`
- **Notifications**:
  - `GET /api/notifications/`
  - `PATCH /api/notifications/<id>/read/`
  - `PUT /api/notifications/mark-all-read/`
  - `DELETE /api/notifications/<id>/`
  - `GET /api/notifications/unread-count/`

## Documentation

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Features

- JWT Authentication
- Real-time bus tracking
- Booking management
- Notification system
- GPS location updates
- WebSocket support (configured)
- Comprehensive API documentation 