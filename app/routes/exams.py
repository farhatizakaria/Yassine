"""
Exam routes for LUS RSIS Management System.
"""
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from app.models import Exam, Student, Module
from . import exams_bp


@exams_bp.route('/', methods=['GET'])
def list_exams():
    """Display list of all exams."""
    page = request.args.get('page', 1, type=int)
    exams = Exam.query.paginate(page=page, per_page=10)
    return render_template('exams/list.html', exams=exams)


@exams_bp.route('/<int:exam_id>', methods=['GET'])
def view_exam(exam_id):
    """View exam details."""
    exam = Exam.query.get_or_404(exam_id)
    return render_template('exams/view.html', exam=exam)


@exams_bp.route('/create', methods=['GET', 'POST'])
def create_exam():
    """Create a new exam."""
    if request.method == 'POST':
        # Validate form data
        exam_code = request.form.get('exam_code', '').strip()
        exam_date_str = request.form.get('exam_date', '')
        duration_minutes = request.form.get('duration_minutes', type=int)
        room_number = request.form.get('room_number', '').strip()
        student_id = request.form.get('student_id', type=int)
        module_id = request.form.get('module_id', type=int)
        
        # Check for duplicate exam code
        if Exam.query.filter_by(exam_code=exam_code).first():
            flash('Exam code already exists.', 'error')
            students = Student.query.all()
            modules = Module.query.all()
            return render_template('exams/create.html', students=students, modules=modules), 400
        
        # Validate required fields
        if not all([exam_code, exam_date_str, duration_minutes, room_number, student_id, module_id]):
            flash('All required fields must be filled.', 'error')
            students = Student.query.all()
            modules = Module.query.all()
            return render_template('exams/create.html', students=students, modules=modules), 400
        
        # Validate student and module exist
        student = Student.query.get(student_id)
        module = Module.query.get(module_id)
        
        if not student:
            flash('Student not found.', 'error')
            students = Student.query.all()
            modules = Module.query.all()
            return render_template('exams/create.html', students=students, modules=modules), 404
        
        if not module:
            flash('Module not found.', 'error')
            students = Student.query.all()
            modules = Module.query.all()
            return render_template('exams/create.html', students=students, modules=modules), 404
        
        # Parse exam date
        try:
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid exam date format.', 'error')
            students = Student.query.all()
            modules = Module.query.all()
            return render_template('exams/create.html', students=students, modules=modules), 400
        
        # Check for scheduling conflicts (same student, same time)
        conflict = Exam.query.filter(
            Exam.student_id == student_id,
            Exam.exam_date == exam_date,
            Exam.status != 'cancelled'
        ).first()
        
        if conflict:
            flash('Scheduling conflict: Student has another exam at this time.', 'error')
            students = Student.query.all()
            modules = Module.query.all()
            return render_template('exams/create.html', students=students, modules=modules), 400
        
        # Check for room availability (same room, overlapping time)
        duration_minutes = int(duration_minutes)
        room_conflict = Exam.query.filter(
            Exam.room_number == room_number,
            Exam.exam_date == exam_date,
            Exam.status != 'cancelled'
        ).first()
        
        if room_conflict:
            flash('Room unavailable at this time.', 'error')
            students = Student.query.all()
            modules = Module.query.all()
            return render_template('exams/create.html', students=students, modules=modules), 400
        
        try:
            exam = Exam(
                exam_code=exam_code,
                exam_date=exam_date,
                duration_minutes=duration_minutes,
                room_number=room_number,
                student_id=student_id,
                module_id=module_id
            )
            db.session.add(exam)
            db.session.commit()
            flash(f'Exam {exam.exam_code} scheduled successfully.', 'success')
            return redirect(url_for('exams.view_exam', exam_id=exam.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating exam: {str(e)}', 'error')
            students = Student.query.all()
            modules = Module.query.all()
            return render_template('exams/create.html', students=students, modules=modules), 500
    
    students = Student.query.all()
    modules = Module.query.all()
    return render_template('exams/create.html', students=students, modules=modules)


@exams_bp.route('/<int:exam_id>/edit', methods=['GET', 'POST'])
def edit_exam(exam_id):
    """Edit exam information."""
    exam = Exam.query.get_or_404(exam_id)
    
    if request.method == 'POST':
        exam.room_number = request.form.get('room_number', '').strip()
        exam.duration_minutes = request.form.get('duration_minutes', type=int)
        exam.score = request.form.get('score', type=float) if request.form.get('score') else None
        exam.status = request.form.get('status', 'scheduled')
        
        if not exam.room_number:
            flash('Room number is required.', 'error')
            return render_template('exams/edit.html', exam=exam), 400
        
        try:
            db.session.commit()
            flash('Exam updated successfully.', 'success')
            return redirect(url_for('exams.view_exam', exam_id=exam.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating exam: {str(e)}', 'error')
            return render_template('exams/edit.html', exam=exam), 500
    
    return render_template('exams/edit.html', exam=exam)


@exams_bp.route('/<int:exam_id>/delete', methods=['POST'])
def delete_exam(exam_id):
    """Delete an exam."""
    exam = Exam.query.get_or_404(exam_id)
    
    try:
        db.session.delete(exam)
        db.session.commit()
        flash('Exam deleted successfully.', 'success')
        return redirect(url_for('exams.list_exams'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting exam: {str(e)}', 'error')
        return redirect(url_for('exams.view_exam', exam_id=exam_id))
