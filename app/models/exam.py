"""
Exam model for LUS RSIS Management System.
"""
from datetime import datetime
from app import db


class Exam(db.Model):
    """Exam model with validation and relationships."""
    
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    exam_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=120)  # Duration in minutes
    room_number = db.Column(db.String(20), nullable=False)
    
    # Foreign keys
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    
    # Exam details
    score = db.Column(db.Float)  # Score out of 20 or 100
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Exam {self.exam_code}: {self.exam_date.strftime("%Y-%m-%d %H:%M")}>'
    
    def to_dict(self):
        """Convert exam record to dictionary."""
        return {
            'id': self.id,
            'exam_code': self.exam_code,
            'exam_date': self.exam_date.strftime('%Y-%m-%d %H:%M') if self.exam_date else None,
            'duration_minutes': self.duration_minutes,
            'room_number': self.room_number,
            'student': self.student.to_dict() if self.student else None,
            'module': self.module.to_dict() if self.module else None,
            'score': self.score,
            'status': self.status,
        }
