# API Documentation

## Overview

MediTech HealthCheckup System provides a comprehensive RESTful API that allows you to interact with all aspects of the system programmatically. This documentation will help you understand how to use these APIs effectively.

## Base URL

All API URLs are relative to:
```
http://localhost:8000/api/v1
```

## Authentication

Most API endpoints require authentication. We use JWT (JSON Web Tokens) for authentication.

### Getting a Token

```http
POST /auth/token
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Using the Token

Include the token in the Authorization header:
```http
Authorization: Bearer your_token_here
```

## API Endpoints

### Health Checkup Management

#### List Health Checkup Packages
```http
GET /packages
```

#### Create Health Checkup Package
```http
POST /packages
Content-Type: application/json

{
    "name": "Basic Checkup",
    "description": "Basic health examination package",
    "price": 2500.00,
    "items": [
        {
            "examination_id": 1,
            "name": "Blood Test",
            "price": 500.00
        }
    ]
}
```

### Patient Management

#### Create Patient
```http
POST /patients
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "contact": {
        "phone": "0812345678",
        "email": "john@example.com"
    }
}
```

#### Get Patient Details
```http
GET /patients/{patient_id}
```

### Appointment Management

#### Create Appointment
```http
POST /appointments
Content-Type: application/json

{
    "patient_id": 1,
    "package_id": 1,
    "appointment_date": "2024-02-01T09:00:00",
    "notes": "First time checkup"
}
```

#### List Appointments
```http
GET /appointments
```

### Medical Records

#### Create Medical Record
```http
POST /records
Content-Type: application/json

{
    "patient_id": 1,
    "appointment_id": 1,
    "vital_signs": {
        "blood_pressure": "120/80",
        "heart_rate": 75,
        "temperature": 36.5
    },
    "examination_results": [
        {
            "item_id": 1,
            "result": "Normal",
            "notes": "Within normal range"
        }
    ]
}
```

#### Get Medical Record
```http
GET /records/{record_id}
```

## Response Format

All responses are returned in JSON format. Successful responses will have a 2xx status code and follow this structure:

```json
{
    "status": "success",
    "data": {
        // Response data here
    }
}
```

Error responses will have a 4xx or 5xx status code and follow this structure:

```json
{
    "status": "error",
    "message": "Error description",
    "code": "ERROR_CODE"
}
```

## Rate Limiting

API requests are limited to:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

## Webhooks

We provide webhooks for real-time notifications:
- Appointment updates
- Examination results
- Report generation

## SDK & Libraries

Official SDKs are available for:
- Python
- JavaScript
- PHP

## Support

For API support:
- Email: api-support@meditech.com
- Documentation: https://docs.meditech.com
- GitHub Issues: https://github.com/BRXG/meditech-healthcheckup/issues 