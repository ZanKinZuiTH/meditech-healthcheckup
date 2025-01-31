from sqlalchemy import Column, String, Integer, Boolean, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base, FullAuditMixin

class Company(Base, FullAuditMixin):
    """
    Model for companies (employers)
    """
    # Basic information
    name = Column(String, nullable=False)
    name_en = Column(String)
    tax_id = Column(String, unique=True)
    business_type = Column(String)
    
    # Contact information
    phone = Column(String)
    fax = Column(String)
    email = Column(String)
    website = Column(String)
    
    # Address
    address = Column(JSON)  # Structured address data
    
    # Company details
    registration_number = Column(String)
    establishment_date = Column(String)
    number_of_employees = Column(Integer)
    
    # Contract information
    contract_number = Column(String)
    contract_start_date = Column(String)
    contract_end_date = Column(String)
    contract_details = Column(JSON)
    
    # Billing information
    billing_address = Column(JSON)
    payment_terms = Column(JSON)
    bank_account = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True)
    status = Column(String, default="active")  # active, inactive, suspended
    remarks = Column(Text)
    
    # Relationships
    employees = relationship("Patient", back_populates="company")
    branches = relationship("CompanyBranch", back_populates="company", cascade="all, delete-orphan")
    contacts = relationship("CompanyContact", back_populates="company", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        """
        Convert company to dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "tax_id": self.tax_id,
            "business_type": self.business_type,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "address": self.address,
            "number_of_employees": self.number_of_employees,
            "contract_number": self.contract_number,
            "contract_start_date": self.contract_start_date,
            "contract_end_date": self.contract_end_date,
            "is_active": self.is_active,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class CompanyBranch(Base, FullAuditMixin):
    """
    Model for company branches
    """
    # Branch information
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String)
    
    # Contact information
    phone = Column(String)
    fax = Column(String)
    email = Column(String)
    
    # Address
    address = Column(JSON)  # Structured address data
    
    # Branch details
    manager_name = Column(String)
    number_of_employees = Column(Integer)
    
    # Status
    is_active = Column(Boolean, default=True)
    remarks = Column(Text)
    
    # Relationships
    company = relationship("Company", back_populates="branches")

    def to_dict(self) -> dict:
        """
        Convert branch to dictionary
        """
        return {
            "id": self.id,
            "company_id": self.company_id,
            "name": self.name,
            "code": self.code,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "manager_name": self.manager_name,
            "number_of_employees": self.number_of_employees,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class CompanyContact(Base, FullAuditMixin):
    """
    Model for company contacts
    """
    # Contact information
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    name = Column(String, nullable=False)
    position = Column(String)
    department = Column(String)
    
    # Contact details
    phone = Column(String)
    mobile = Column(String)
    email = Column(String)
    line_id = Column(String)
    
    # Role
    is_primary = Column(Boolean, default=False)
    contact_type = Column(String)  # billing, technical, management
    
    # Status
    is_active = Column(Boolean, default=True)
    remarks = Column(Text)
    
    # Relationships
    company = relationship("Company", back_populates="contacts")

    def to_dict(self) -> dict:
        """
        Convert contact to dictionary
        """
        return {
            "id": self.id,
            "company_id": self.company_id,
            "name": self.name,
            "position": self.position,
            "department": self.department,
            "phone": self.phone,
            "mobile": self.mobile,
            "email": self.email,
            "is_primary": self.is_primary,
            "contact_type": self.contact_type,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class InsuranceCompany(Base, FullAuditMixin):
    """
    Model for insurance companies
    """
    # Company information
    name = Column(String, nullable=False)
    name_en = Column(String)
    license_number = Column(String)
    tax_id = Column(String)
    
    # Contact information
    phone = Column(String)
    fax = Column(String)
    email = Column(String)
    website = Column(String)
    
    # Address
    address = Column(JSON)  # Structured address data
    
    # Contract information
    contract_number = Column(String)
    contract_details = Column(JSON)
    service_level_agreement = Column(JSON)
    
    # Financial information
    payment_terms = Column(JSON)
    bank_account = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True)
    remarks = Column(Text)
    
    # Relationships
    checkup_jobs = relationship("CheckupJob", back_populates="insurance_company")

    def to_dict(self) -> dict:
        """
        Convert insurance company to dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "license_number": self.license_number,
            "tax_id": self.tax_id,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "address": self.address,
            "contract_number": self.contract_number,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 