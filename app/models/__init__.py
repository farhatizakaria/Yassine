"""
Database models for LUS RSIS Management System.
"""
from .student import Student
from .teacher import Teacher
from .module import Module
from .exam import Exam

__all__ = ['Student', 'Teacher', 'Module', 'Exam']
