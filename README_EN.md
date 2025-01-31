# 🏥 MediTech HealthCheckup System

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-green.svg)](https://fastapi.tiangolo.com/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.0%2B-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![GitHub license](https://img.shields.io/github/license/BRXG/meditech-healthcheckup)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/BRXG/meditech-healthcheckup)](https://github.com/BRXG/meditech-healthcheckup/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/BRXG/meditech-healthcheckup)](https://github.com/BRXG/meditech-healthcheckup/network)
[![GitHub issues](https://img.shields.io/github/issues/BRXG/meditech-healthcheckup)](https://github.com/BRXG/meditech-healthcheckup/issues)

A comprehensive health checkup and medical record management system developed with Python.

[English](README_EN.md) | [ภาษาไทย](README.md)

![MediTech HealthCheckup Screenshot](docs/images/screenshot.png)

## 📖 Project Description

MediTech HealthCheckup System is a modern solution for managing health checkups and medical records, built with cutting-edge technologies:

- **Backend**: Developed with FastAPI for high performance and speed
- **Frontend**: Built with PyQt6 for a beautiful and user-friendly desktop application
- **Database**: PostgreSQL for stable and secure data storage
- **Architecture**: MVVM (Model-View-ViewModel) pattern for clear separation of concerns

## ✨ Key Features

### 🏥 Health Checkup System
- Health Checkup Management
  - Create and manage health checkup packages
  - Define examination items and pricing
  - Schedule appointments
- Record and Track Results
  - Real-time examination recording
  - Abnormal result notifications
  - Examination status tracking
- Result Summary Reports
  - Generate PDF reports
  - Comparative analysis graphs
  - Export data in various formats
- Corporate Client Management
  - Organization membership system
  - Benefits management
  - Automatic invoice generation

### 📋 Electronic Medical Record (EMR)
- Treatment History
  - Medical history
  - Drug allergy history
  - Family history
- Patient Information
  - Personal information
  - Appointment history
  - Treatment tracking
- Vital Signs
  - Measure and record values
  - Abnormal value alerts
  - Trend graphs
- Treatment Tracking
  - Treatment timeline
  - Medication history
  - Follow-up appointments

## 🎓 For Students

### Code Study Guide
1. Understanding Project Structure:
   - `backend/`: API endpoints and business logic
   - `frontend/`: UI and state management
   - `Models/`: Data structures and relationships
   - `ViewModels/`: Model and View connections
   - `Services/`: Business service operations

2. Design Patterns Used:
   - MVVM Pattern
   - Repository Pattern
   - Factory Pattern
   - Observer Pattern
   - Dependency Injection

3. Technology Stack:
   - FastAPI: API development
   - PyQt6: Desktop UI development
   - SQLAlchemy: Database management
   - Pydantic: Data validation

### Development Guidelines
1. New Features:
   - Online appointment system
   - Online payment
   - LINE notifications
   - Mobile application

2. Performance Improvements:
   - Add caching
   - Optimize database queries
   - Implement load balancing
   - Add real-time features

3. Security Enhancements:
   - Implement 2FA
   - Add audit logging
   - Enhance data encryption
   - Improve access control

4. UI/UX Development:
   - Create responsive design
   - Add dark mode
   - Improve accessibility
   - Create interactive reports

## 📝 Copyright

© 2024 BRXG Co., Ltd.

## 🚀 Installation

### System Requirements
- Python 3.9+
- PostgreSQL 13+
- Git

### Installation Steps

1. Clone repository:
```bash
git clone https://github.com/BRXG/meditech-healthcheckup.git
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

4. Set up environment:
```bash
cp .env.example .env
# Edit .env file as needed
```

5. Run with Docker:
```bash
docker-compose up -d
```

## 🤝 Contributing

We welcome community contributions! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📝 License

© 2024 BRXG Co., Ltd.

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 👥 Development Team

Developed by BRXG Co., Ltd.

## 📞 Contact

- Website: https://brxggroup.com
- Facebook: https://www.facebook.com/brxggroup/?locale=th_TH
- GitHub Issues: https://github.com/BRXG/meditech-healthcheckup/issues

## 🙏 Acknowledgments

Thanks to:
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyQt](https://www.riverbankcomputing.com/software/pyqt/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [And more](ACKNOWLEDGMENTS.md) 