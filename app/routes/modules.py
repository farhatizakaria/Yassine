"""
Module routes for LUS RSIS Management System.
"""
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Module, Teacher
from . import modules_bp


@modules_bp.route('/', methods=['GET'])
def list_modules():
    """Display list of all modules."""
    page = request.args.get('page', 1, type=int)
    modules = Module.query.paginate(page=page, per_page=10)
    return render_template('modules/list.html', modules=modules)


@modules_bp.route('/<int:module_id>', methods=['GET'])
def view_module(module_id):
    """View module details."""
    module = Module.query.get_or_404(module_id)
    return render_template('modules/view.html', module=module)


@modules_bp.route('/create', methods=['GET', 'POST'])
def create_module():
    """Create a new module."""
    if request.method == 'POST':
        # Validate form data
        code = request.form.get('code', '').strip()
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        credits = request.form.get('credits', type=int)
        semester = request.form.get('semester', type=int)
        workload_hours = request.form.get('workload_hours', type=int)
        teacher_id = request.form.get('teacher_id', type=int)
        
        # Check for duplicate module code
        if Module.query.filter_by(code=code).first():
            flash('Module code already exists.', 'error')
            teachers = Teacher.query.all()
            return render_template('modules/create.html', teachers=teachers), 400
        
        # Validate required fields
        if not all([code, name, credits, semester, workload_hours, teacher_id]):
            flash('All required fields must be filled.', 'error')
            teachers = Teacher.query.all()
            return render_template('modules/create.html', teachers=teachers), 400
        
        # Validate semester range
        if semester < 1 or semester > 6:
            flash('Semester must be between 1 and 6.', 'error')
            teachers = Teacher.query.all()
            return render_template('modules/create.html', teachers=teachers), 400
        
        # Check teacher workload
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            flash('Teacher not found.', 'error')
            teachers = Teacher.query.all()
            return render_template('modules/create.html', teachers=teachers), 404
        
        if not teacher.can_add_module(workload_hours):
            flash(f'Teacher workload exceeded. Available: {teacher.max_workload - teacher.workload_hours} hours.', 'error')
            teachers = Teacher.query.all()
            return render_template('modules/create.html', teachers=teachers), 400
        
        try:
            module = Module(
                code=code,
                name=name,
                description=description,
                credits=credits,
                semester=semester,
                workload_hours=workload_hours,
                teacher_id=teacher_id
            )
            teacher.workload_hours += workload_hours
            db.session.add(module)
            db.session.commit()
            flash(f'Module {module.code} created successfully.', 'success')
            return redirect(url_for('modules.view_module', module_id=module.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating module: {str(e)}', 'error')
            teachers = Teacher.query.all()
            return render_template('modules/create.html', teachers=teachers), 500
    
    teachers = Teacher.query.all()
    return render_template('modules/create.html', teachers=teachers)


@modules_bp.route('/<int:module_id>/edit', methods=['GET', 'POST'])
def edit_module(module_id):
    """Edit module information."""
    module = Module.query.get_or_404(module_id)
    
    if request.method == 'POST':
        old_workload = module.workload_hours
        module.name = request.form.get('name', '').strip()
        module.description = request.form.get('description', '').strip()
        module.credits = request.form.get('credits', type=int)
        module.workload_hours = request.form.get('workload_hours', type=int)
        
        if not all([module.name, module.credits, module.workload_hours]):
            flash('Required fields must be filled.', 'error')
            return render_template('modules/edit.html', module=module), 400
        
        # Check workload if changed
        if module.workload_hours != old_workload:
            workload_diff = module.workload_hours - old_workload
            if not module.teacher.can_add_module(workload_diff):
                flash('Teacher workload exceeded.', 'error')
                return render_template('modules/edit.html', module=module), 400
            module.teacher.workload_hours += workload_diff
        
        try:
            db.session.commit()
            flash('Module updated successfully.', 'success')
            return redirect(url_for('modules.view_module', module_id=module.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating module: {str(e)}', 'error')
            return render_template('modules/edit.html', module=module), 500
    
    return render_template('modules/edit.html', module=module)


@modules_bp.route('/<int:module_id>/delete', methods=['POST'])
def delete_module(module_id):
    """Delete a module."""
    module = Module.query.get_or_404(module_id)
    
    try:
        # Restore teacher's workload
        module.teacher.workload_hours -= module.workload_hours
        db.session.delete(module)
        db.session.commit()
        flash('Module deleted successfully.', 'success')
        return redirect(url_for('modules.list_modules'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting module: {str(e)}', 'error')
        return redirect(url_for('modules.view_module', module_id=module_id))
