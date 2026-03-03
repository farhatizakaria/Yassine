"""
Student model for LUS RSIS Management System.
"""
from datetime import datetime
from app import db


class Student(db.Model):
    """Student model with validation and relationships."""
    
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with exams
    exams = db.relationship('Exam', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.student_id}: {self.first_name} {self.last_name}>'
    
    def to_dict(self):
        """Convert student record to dictionary."""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'enrollment_date': self.enrollment_date.strftime('%Y-%m-%d') if self.enrollment_date else None,
        }
