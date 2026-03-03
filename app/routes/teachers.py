"""
Teacher routes for LUS RSIS Management System.
"""
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Teacher
from . import teachers_bp


@teachers_bp.route('/', methods=['GET'])
def list_teachers():
    """Display list of all teachers."""
    page = request.args.get('page', 1, type=int)
    teachers = Teacher.query.paginate(page=page, per_page=10)
    return render_template('teachers/list.html', teachers=teachers)


@teachers_bp.route('/<int:teacher_id>', methods=['GET'])
def view_teacher(teacher_id):
    """View teacher details."""
    teacher = Teacher.query.get_or_404(teacher_id)
    return render_template('teachers/view.html', teacher=teacher)


@teachers_bp.route('/create', methods=['GET', 'POST'])
def create_teacher():
    """Create a new teacher."""
    if request.method == 'POST':
        # Validate form data
        matricule = request.form.get('matricule', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        department = request.form.get('department', '').strip()
        office = request.form.get('office', '').strip()
        
        # Check for duplicate matricule or email
        if Teacher.query.filter_by(matricule=matricule).first():
            flash('Teacher matricule already exists.', 'error')
            return render_template('teachers/create.html'), 400
        
        if Teacher.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('teachers/create.html'), 400
        
        # Validate required fields
        if not all([matricule, first_name, last_name, email, department]):
            flash('All required fields must be filled.', 'error')
            return render_template('teachers/create.html'), 400
        
        try:
            teacher = Teacher(
                matricule=matricule,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                department=department,
                office=office
            )
            db.session.add(teacher)
            db.session.commit()
            flash(f'Teacher {teacher.matricule} created successfully.', 'success')
            return redirect(url_for('teachers.view_teacher', teacher_id=teacher.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating teacher: {str(e)}', 'error')
            return render_template('teachers/create.html'), 500
    
    return render_template('teachers/create.html')


@teachers_bp.route('/<int:teacher_id>/edit', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    """Edit teacher information."""
    teacher = Teacher.query.get_or_404(teacher_id)
    
    if request.method == 'POST':
        teacher.first_name = request.form.get('first_name', '').strip()
        teacher.last_name = request.form.get('last_name', '').strip()
        teacher.phone = request.form.get('phone', '').strip()
        teacher.office = request.form.get('office', '').strip()
        
        if not all([teacher.first_name, teacher.last_name]):
            flash('Required fields must be filled.', 'error')
            return render_template('teachers/edit.html', teacher=teacher), 400
        
        try:
            db.session.commit()
            flash('Teacher updated successfully.', 'success')
            return redirect(url_for('teachers.view_teacher', teacher_id=teacher.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating teacher: {str(e)}', 'error')
            return render_template('teachers/edit.html', teacher=teacher), 500
    
    return render_template('teachers/edit.html', teacher=teacher)


@teachers_bp.route('/<int:teacher_id>/delete', methods=['POST'])
def delete_teacher(teacher_id):
    """Delete a teacher."""
    teacher = Teacher.query.get_or_404(teacher_id)
    
    try:
        db.session.delete(teacher)
        db.session.commit()
        flash('Teacher deleted successfully.', 'success')
        return redirect(url_for('teachers.list_teachers'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting teacher: {str(e)}', 'error')
        return redirect(url_for('teachers.view_teacher', teacher_id=teacher_id))
