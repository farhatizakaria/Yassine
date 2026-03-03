"""
Student routes for LUS RSIS Management System.
"""
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Student
from . import students_bp


@students_bp.route('/', methods=['GET'])
def list_students():
    """Display list of all students."""
    page = request.args.get('page', 1, type=int)
    students = Student.query.paginate(page=page, per_page=10)
    return render_template('students/list.html', students=students)


@students_bp.route('/<int:student_id>', methods=['GET'])
def view_student(student_id):
    """View student details."""
    student = Student.query.get_or_404(student_id)
    return render_template('students/view.html', student=student)


@students_bp.route('/create', methods=['GET', 'POST'])
def create_student():
    """Create a new student."""
    if request.method == 'POST':
        # Validate form data
        student_id = request.form.get('student_id', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Check for duplicate student ID or email
        if Student.query.filter_by(student_id=student_id).first():
            flash('Student ID already exists.', 'error')
            return render_template('students/create.html'), 400
        
        if Student.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('students/create.html'), 400
        
        # Validate required fields
        if not all([student_id, first_name, last_name, email]):
            flash('All required fields must be filled.', 'error')
            return render_template('students/create.html'), 400
        
        try:
            student = Student(
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
            db.session.add(student)
            db.session.commit()
            flash(f'Student {student.student_id} created successfully.', 'success')
            return redirect(url_for('students.view_student', student_id=student.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating student: {str(e)}', 'error')
            return render_template('students/create.html'), 500
    
    return render_template('students/create.html')


@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    """Edit student information."""
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        student.first_name = request.form.get('first_name', '').strip()
        student.last_name = request.form.get('last_name', '').strip()
        student.phone = request.form.get('phone', '').strip()
        
        if not all([student.first_name, student.last_name]):
            flash('Required fields must be filled.', 'error')
            return render_template('students/edit.html', student=student), 400
        
        try:
            db.session.commit()
            flash('Student updated successfully.', 'success')
            return redirect(url_for('students.view_student', student_id=student.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'error')
            return render_template('students/edit.html', student=student), 500
    
    return render_template('students/edit.html', student=student)


@students_bp.route('/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    """Delete a student."""
    student = Student.query.get_or_404(student_id)
    
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully.', 'success')
        return redirect(url_for('students.list_students'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'error')
        return redirect(url_for('students.view_student', student_id=student_id))
