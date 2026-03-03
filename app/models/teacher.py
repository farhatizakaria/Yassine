"""
Teacher model for LUS RSIS Management System.
"""
from datetime import datetime
from app import db


class Teacher(db.Model):
    """Teacher model with validation and relationships."""
    
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100), nullable=False)
    office = db.Column(db.String(50))
    workload_hours = db.Column(db.Integer, default=0)
    max_workload = db.Column(db.Integer, default=24)  # Default max hours per semester
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with modules (many-to-many handled through Module)
    modules = db.relationship('Module', backref='teacher', lazy=True)
    
    def __repr__(self):
        return f'<Teacher {self.matricule}: {self.first_name} {self.last_name}>'
    
    def to_dict(self):
        """Convert teacher record to dictionary."""
        return {
            'id': self.id,
            'matricule': self.matricule,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'office': self.office,
            'workload_hours': self.workload_hours,
        }
    
    def can_add_module(self, hours):
        """Check if teacher can take on additional workload."""
        return (self.workload_hours + hours) <= self.max_workload
