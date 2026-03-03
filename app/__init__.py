"""
Flask application factory for LUS RSIS Management System.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name='development'):
    """
    Create and configure the Flask application.
    
    Args:
        config_name (str): Configuration environment name
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)

    # Import models so that SQLAlchemy knows about them before creating tables.
    # models are imported lazily by the blueprints later, but create_all is
    # called before the blueprints are registered which meant no tables were
    # created (SQLite would create an empty file). Importing here ensures all
    # model metadata is registered.
    from app import models  # noqa: F401 - import triggers model definitions

    # Register database context and create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import students_bp, teachers_bp, modules_bp, exams_bp, main_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(exams_bp)
    
    return app
