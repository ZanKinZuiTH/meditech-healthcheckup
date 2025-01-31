# 🏥 MediTech HealthCheckup System

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-green.svg)](https://fastapi.tiangolo.com/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.0%2B-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)

A comprehensive healthcare management and medical record system developed with Python

[English](README_EN.md) | [ภาษาไทย](README.md)

![MediTech HealthCheckup Screenshot](docs/images/screenshot.png)

## 📖 Project Description

MediTech HealthCheckup System is a comprehensive solution for managing health checkups and medical records, built with modern technologies:

- **Backend**: Developed with FastAPI, a high-performance and fast framework
- **Frontend**: Built with PyQt6 for a user-friendly and beautiful Desktop Application
- **Database**: PostgreSQL as the main database for stability and security
- **Architecture**: Utilizes MVVM (Model-View-ViewModel) pattern for clear separation of concerns

## ✨ Key Features

### 🏥 Health Checkup System
- Health Checkup Management
  - Create and manage health checkup packages
  - Define examination items and pricing
  - Schedule appointments
- Record and Track Results
  - Real-time result recording
  - Abnormal result alert system
  - Examination status tracking
- Summary Reports
  - Generate PDF reports
  - Comparative result graphs
  - Export data in various formats
- Corporate Client Management
  - Organization membership system
  - Benefit management
  - Automatic invoice generation

### 📋 Electronic Medical Record (EMR)
- Medical History Recording
  - Illness history
  - Drug allergy history
  - Family history
- Patient Information Management
  - Personal information
  - Appointment history
  - Treatment tracking
- Vital Signs Recording
  - Measure and record values
  - Abnormal value alerts
  - Trend graphs
- Treatment History Tracking
  - Treatment timeline
  - Medication history
  - Follow-up appointments

## 🎓 For Students

### Code Study Guide
1. Start by understanding the project structure:
   - `backend/`: Study API endpoints and business logic
   - `frontend/`: Learn UI creation and state management
   - `Models/`: Study data structures and relationships
   - `ViewModels/`: Understand Model-View connections
   - `Services/`: Study business service operations

2. Understand Design Patterns Used:
   - MVVM Pattern
   - Repository Pattern
   - Factory Pattern
   - Observer Pattern
   - Dependency Injection

3. Study Technology Usage:
   - FastAPI: Creating API endpoints
   - PyQt6: Desktop UI development
   - SQLAlchemy: Database management
   - Pydantic: Data validation

### Development Extension Guide
1. Add New Features:
   - Online appointment system
   - Online payment
   - LINE notification system
   - Mobile Application

2. Performance Improvements:
   - Add Caching
   - Optimize Database Queries
   - Implement Load Balancing
   - Add Real-time Features

3. Security Enhancements:
   - Implement 2FA
   - Add Audit Logging
   - Enhance Data Encryption
   - Improve Access Control

4. UI/UX Development:
   - Create Responsive Design
   - Add Dark Mode
   - Improve Accessibility
   - Create Interactive Reports

## 🚀 Installation

### System Requirements
- Python 3.9+
- PostgreSQL 13+
- Git

### Installation Steps

1. Clone repository:
```bash
git clone https://github.com/yourusername/meditech-healthcheckup.git
cd meditech-healthcheckup
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup database:
```bash
cd backend
alembic upgrade head
```

5. Run application:
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
python main.py
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Development Guide](docs/development_guide.md)
- [Database Schema](docs/database_schema.md)
- [API Documentation](docs/api/README.md)
- [User Guide](docs/user_guide/README.md)

## 🔧 Development

### Project Structure
```
meditech_healthcheckup/
├── backend/              # FastAPI Backend
├── frontend/            # PyQt6 Desktop Application
├── docs/               # Documentation
└── tests/              # Unit & Integration Tests
```

### Development Environment Setup
1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Setup pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
pytest
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Create Pull Request

Read more details in [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 Copyright and License

© 2024 BRXG Co. All rights reserved.

The MediTech HealthCheckup System and all its components are the exclusive intellectual property of BRXG Co. Any use, reproduction, modification, or distribution of any part of this project requires written permission from BRXG Co.

### Company Contact
- Website: https://brxggroup.com
- Facebook: https://www.facebook.com/brxggroup/?locale=th_TH

## 👥 Development Team

- Developer 1 - [GitHub](https://github.com/developer1)
- Developer 2 - [GitHub](https://github.com/developer2)

## 📞 Contact

- Email: support@meditech.com
- Website: https://meditech.com
- Tel: 02-XXX-XXXX

## 🙏 Acknowledgments

Thanks to:
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyQt](https://www.riverbankcomputing.com/software/pyqt/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [And others](ACKNOWLEDGMENTS.md) 