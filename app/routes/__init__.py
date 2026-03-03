"""
Routes blueprints for LUS RSIS Management System.
"""
from flask import Blueprint

# Create blueprints
main_bp = Blueprint('main', __name__)
students_bp = Blueprint('students', __name__, url_prefix='/students')
teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')
modules_bp = Blueprint('modules', __name__, url_prefix='/modules')
exams_bp = Blueprint('exams', __name__, url_prefix='/exams')

# Import route handlers
from . import main, students, teachers, modules, exams

__all__ = ['main_bp', 'students_bp', 'teachers_bp', 'modules_bp', 'exams_bp']
