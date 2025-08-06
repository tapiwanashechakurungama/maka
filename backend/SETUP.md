# Django Backend Setup Guide

This guide ensures that user registration and login work properly in the MSU Bus Tracking System.

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Setup Script
```bash
python setup.py
```

This script will:
- ✅ Check database connection
- ✅ Verify model configuration
- ✅ Create and apply migrations
- ✅ Test user creation
- ✅ Create admin superuser
- ✅ Verify URL configuration

### 3. Start the Server
```bash
python manage.py runserver
```

## 🧪 Testing

### Test Authentication
```bash
python test_auth.py
```

### Test End-to-End
```bash
python test_end_to_end.py
```

### Test API Endpoints
```bash
python test_api.py
```

## 📱 Mobile App Integration

The Django backend is configured to work with the mobile app:

### Registration Format
```json
{
  "firstName": "John",
  "lastName": "Doe", 
  "email": "john@example.com",
  "password": "password123"
}
```

### Login Format
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

### Response Format
```json
{
  "token": "jwt_access_token",
  "refresh": "jwt_refresh_token",
  "user": {
    "id": 1,
    "username": "john@example.com",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

## 🔐 Admin Access

After running `setup.py`, you can access the admin panel:

- **URL**: http://localhost:8000/admin/
- **Username**: admin
- **Email**: admin@msu.ac.zw
- **Password**: admin123

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Health Check**: http://localhost:8000/api/health/

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure SQLite file is writable
   - Check file permissions

2. **Migration Errors**
   - Delete `migrations/` folder (except `__init__.py`)
   - Run `python setup.py` again

3. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python environment

4. **Authentication Errors**
   - Verify JWT settings in `settings.py`
   - Check token expiration settings

### Debug Mode

For debugging, set `DEBUG = True` in `Core/settings.py` and check:
- Django logs in console
- Browser network tab for API calls
- Mobile app console for errors

## ✅ Verification Checklist

- [ ] Dependencies installed
- [ ] Database migrations applied
- [ ] Admin superuser created
- [ ] Health check endpoint working
- [ ] Registration endpoint working
- [ ] Login endpoint working
- [ ] JWT tokens generated correctly
- [ ] Mobile app can connect to API
- [ ] Authenticated requests working

## 🎯 Next Steps

1. **Test with Mobile App**
   - Start Django server
   - Run mobile app
   - Test registration and login

2. **Production Setup**
   - Change `DEBUG = False`
   - Set up production database
   - Configure environment variables
   - Set up HTTPS

3. **Deployment**
   - Choose hosting platform
   - Set up CI/CD pipeline
   - Configure domain and SSL 