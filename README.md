# LUS RSIS Management System

This is a comprehensive academic management system built with Flask for managing:
- Students
- Teachers
- Modules
- Exams

## Installation

The project is designed to work the same on Linux, macOS and Windows. You
can perform the setup manually or use the bundled `bootstrap.py` helper which
creates a virtual environment, installs the dependencies and prints the
commands you need to start the server.

### Automatic (recommended)

```bash
# run this with the system python; it will create `venv` if it's missing
python bootstrap.py
```

Once the script completes you will see output such as:

```
Setup complete. To run:
    source venv/bin/activate           # or `venv\Scripts\activate` on Windows
    python run.py
```

### Manual steps

1. Create a virtual environment (works on all platforms):

   ```bash
   python3 -m venv venv
   ```

2. Activate it:

   **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   **Windows (PowerShell or cmd):**
   ```bash
   venv\Scripts\activate
   ```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python run.py
```

The app will start at `http://localhost:5000`.

## Database

The application uses SQLite by default. The database file (`lus_rsis.db`) will be created automatically on first run and all tables are created by the application factory.

> **Note:** If you previously started the app before the models were imported you may end up with an empty database file that contains no tables. If you see errors like `sqlite3.OperationalError: no such table: students`, delete `lus_rsis.db` and restart the app (or open a Flask shell and run `from app import db; db.create_all()`).

To use a different database, update the `DATABASE_URL` in `config.py`:

```python
# PostgreSQL example
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/lus_rsis'

# MySQL example  
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/lus_rsis'
```

## Project Structure

```
app/
├── models/          # Database models (Student, Teacher, Module, Exam)
├── routes/          # Flask blueprints for different modules
├── templates/       # HTML templates
│   ├── students/
│   ├── teachers/
│   ├── modules/
│   └── exams/
└── static/          # CSS, JavaScript, images
    ├── css/
    └── js/

config.py           # Configuration settings
run.py              # Application entry point
requirements.txt    # Python dependencies
```

## Features

- **Student Management**: Add, edit, delete, and view student information
- **Teacher Management**: Manage teacher profiles and workload
- **Module Management**: Define modules and assign teachers with workload validation
- **Exam Scheduling**: Schedule exams with conflict detection
  - Prevents student scheduling conflicts
  - Prevents room allocation conflicts
- **Clean UI**: Simple, professional interface for academic staff
- **Data Validation**: Server-side validation for all inputs
- **Error Handling**: Proper error messages and HTTP status codes

## Technologies Used

- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy ORM with SQLite (configurable)
- **Frontend**: HTML5, CSS3, JavaScript
- **Templating**: Jinja2
- **Python**: 3.8+

## Configuration

Create a `.env` file in the root directory:

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///lus_rsis.db
```

## Security Notes

- All inputs are validated server-side
- Database queries use ORM to prevent SQL injection
- CSRF protection for forms
- Sensitive data is not exposed in responses

## Future Enhancements

- User authentication and role-based access control
- REST API endpoints
- Dashboard statistics and analytics
- PDF/Excel export functionality
- Email notifications
- Unit and integration tests
- Docker containerization

## License

This project is part of the LUS RSIS academic management initiative.
