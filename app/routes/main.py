"""
Main routes for LUS RSIS Management System.
"""
from flask import render_template
from . import main_bp


@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page with summary statistics.

    Pulls counts from the database so the numbers update whenever records
    are added/removed. Values are passed into the template where the
    cards display them.
    """
    # avoid circular import by importing models here
    from app.models.student import Student
    from app.models.teacher import Teacher
    from app.models.module import Module
    from app.models.exam import Exam

    student_count = Student.query.count()
    teacher_count = Teacher.query.count()
    module_count = Module.query.count()
    exam_count = Exam.query.count()

    return render_template(
        'dashboard.html',
        student_count=student_count,
        teacher_count=teacher_count,
        module_count=module_count,
        exam_count=exam_count,
    )


@main_bp.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500
