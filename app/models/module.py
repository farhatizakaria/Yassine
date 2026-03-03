"""
Module model for LUS RSIS Management System.
"""
from datetime import datetime
from app import db


class Module(db.Model):
    """Module model with validation and relationships."""
    
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)  # 1-6
    workload_hours = db.Column(db.Integer, nullable=False)  # Hours per week
    
    # Foreign key to teacher
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with exams
    exams = db.relationship('Exam', backref='module', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Module {self.code}: {self.name}>'
    
    def to_dict(self):
        """Convert module record to dictionary."""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'credits': self.credits,
            'semester': self.semester,
            'workload_hours': self.workload_hours,
            'teacher': self.teacher.to_dict() if self.teacher else None,
        }
