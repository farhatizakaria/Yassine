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
    """Dashboard page."""
    return render_template('dashboard.html')


@main_bp.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500
