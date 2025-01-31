# API Documentation

## Overview

MediTech HealthCheckup System API provides RESTful endpoints for managing health checkups, medical records, and system operations.

Base URL: `http://api.meditech.com/v1`

## Authentication

All API requests require authentication using JWT (JSON Web Token).

### Headers
```
Authorization: Bearer <token>
```

## Endpoints

### 🏥 Health Checkup

#### Packages
- `GET /packages` - List all health checkup packages
- `POST /packages` - Create new package
- `GET /packages/{id}` - Get package details
- `PUT /packages/{id}` - Update package
- `DELETE /packages/{id}` - Delete package

#### Appointments
- `GET /appointments` - List appointments
- `POST /appointments` - Create appointment
- `GET /appointments/{id}` - Get appointment details
- `PUT /appointments/{id}` - Update appointment
- `DELETE /appointments/{id}` - Cancel appointment

#### Examination Results
- `GET /examinations` - List examination results
- `POST /examinations` - Record new result
- `GET /examinations/{id}` - Get result details
- `PUT /examinations/{id}` - Update result
- `POST /examinations/{id}/files` - Upload result files

### 📋 Medical Records

#### Patients
- `GET /patients` - List patients
- `POST /patients` - Register new patient
- `GET /patients/{id}` - Get patient details
- `PUT /patients/{id}` - Update patient info
- `GET /patients/{id}/history` - Get medical history

#### Vital Signs
- `GET /vitals` - List vital records
- `POST /vitals` - Record new vitals
- `GET /vitals/{id}` - Get vital details
- `GET /vitals/{patient_id}/trends` - Get vital trends

### 📊 Reports

#### Health Reports
- `GET /reports/health` - List health reports
- `POST /reports/health` - Generate new report
- `GET /reports/health/{id}` - Get report details
- `GET /reports/health/{id}/pdf` - Download PDF
- `GET /reports/health/{id}/excel` - Download Excel

#### Statistics
- `GET /reports/stats/patients` - Patient statistics
- `GET /reports/stats/examinations` - Examination statistics
- `GET /reports/stats/appointments` - Appointment statistics
- `GET /reports/stats/trends` - Trend analysis

### 🎨 UI/UX Settings

#### Themes
- `GET /settings/themes` - List available themes
- `POST /settings/themes` - Create custom theme
- `GET /settings/themes/{id}` - Get theme details
- `PUT /settings/themes/{id}` - Update theme

#### Accessibility
- `GET /settings/accessibility` - Get accessibility settings
- `PUT /settings/accessibility` - Update settings
- `GET /settings/languages` - List available languages
- `PUT /settings/languages` - Update language preference

## Request/Response Examples

### Create Appointment

Request:
```json
POST /appointments
{
  "patient_id": "123",
  "package_id": "456",
  "datetime": "2024-02-01T10:00:00Z",
  "notes": "Annual checkup"
}
```

Response:
```json
{
  "id": "789",
  "patient_id": "123",
  "package_id": "456",
  "datetime": "2024-02-01T10:00:00Z",
  "status": "scheduled",
  "notes": "Annual checkup",
  "created_at": "2024-01-31T15:00:00Z"
}
```

### Record Examination Result

Request:
```json
POST /examinations
{
  "appointment_id": "789",
  "type": "blood_pressure",
  "values": {
    "systolic": 120,
    "diastolic": 80
  },
  "notes": "Normal range"
}
```

Response:
```json
{
  "id": "321",
  "appointment_id": "789",
  "type": "blood_pressure",
  "values": {
    "systolic": 120,
    "diastolic": 80
  },
  "status": "completed",
  "notes": "Normal range",
  "recorded_at": "2024-02-01T10:15:00Z"
}
```

### Generate Report

Request:
```json
POST /reports/health
{
  "patient_id": "123",
  "type": "comprehensive",
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-01-31"
  },
  "format": "pdf"
}
```

Response:
```json
{
  "id": "654",
  "patient_id": "123",
  "type": "comprehensive",
  "status": "generated",
  "download_url": "/reports/health/654/pdf",
  "generated_at": "2024-01-31T15:30:00Z"
}
```

## Error Handling

### Error Codes
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "datetime",
        "message": "Must be a future date"
      }
    ]
  }
}
```

## Rate Limiting

- Rate limit: 1000 requests per hour
- Rate limit header: `X-RateLimit-Limit`
- Remaining requests: `X-RateLimit-Remaining`
- Reset time: `X-RateLimit-Reset`

## Webhooks

### Available Events
- `appointment.created`
- `appointment.updated`
- `examination.completed`
- `report.generated`

### Webhook Payload
```json
{
  "event": "appointment.created",
  "timestamp": "2024-01-31T15:00:00Z",
  "data": {
    "id": "789",
    "patient_id": "123",
    "status": "scheduled"
  }
}
```

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