---
description: These instructions should be loaded whenever working on the LUS RSIS Web Management Application (student, teacher, module, or exam management system).
applyTo: "**/*.py, **/*.html, **/*.css, **/*.js"
---

# 📘 Project Instructions – LUS RSIS Management Application

## 1️⃣ Project Context

This project is a **Web Application for Managing Academic Activities** within LUS RSIS.

The application manages:

- 👨‍🎓 Students  
- 👨‍🏫 Teachers  
- 📚 Modules  
- 📝 Exams  

The goal is to build a structured, maintainable, and scalable academic management system using:

- **Python**
- **Flask or Django**
- **HTML templates**
- Relational Database (SQLite / PostgreSQL / MySQL)

The AI must generate production-ready, clean, and structured code that respects good software engineering practices.

---

# 2️⃣ General Development Principles

When generating or reviewing code, the AI must:

- Follow clean architecture principles
- Use clear naming conventions (English only for code)
- Avoid unnecessary complexity
- Keep functions small and focused
- Add comments where logic is not obvious
- Ensure proper validation and error handling
- Never leave placeholder logic unfinished

---

# 3️⃣ Project Architecture Guidelines

## If Using Flask:

- Use modular structure:
/app
/models
/routes
/templates
/static
init.py
config.py
run.py


- Use Blueprints for separation of concerns
- Use Jinja2 templating properly
- Keep business logic outside routes when possible

## If Using Django:

- Use separate apps:
- students
- teachers
- modules
- exams

- Follow Django MTV architecture
- Keep logic inside models/services, not in views
- Use Django forms for validation

---

# 4️⃣ Database Design Guidelines

- Use relational models with proper foreign keys
- Enforce uniqueness constraints:
- Student ID → unique
- Teacher matricule → unique
- Module code → unique
- Use proper relationships:
- Teacher ↔ Modules (One-to-Many or Many-to-Many)
- Student ↔ Exams
- Module ↔ Exams

- Never duplicate data unnecessarily
- Use migrations properly (Django) or structured models (Flask SQLAlchemy)

---

# 5️⃣ Coding Standards

## Python Rules

- Follow PEP8
- Use snake_case for variables and functions
- Use PascalCase for classes
- Validate all user inputs
- Never trust frontend data
- Raise meaningful exceptions

## HTML Rules

- Keep templates simple and readable
- Avoid inline CSS/JS
- Use template inheritance (base.html)
- Display error messages clearly

## Error Handling

The system must properly handle:

### Students
- Duplicate ID
- Missing required fields
- Invalid email format
- Student not found

### Teachers
- Existing matricule
- Invalid email
- Workload exceeded
- Teacher not found

### Modules
- Duplicate module code
- Missing fields
- Assignment conflict
- Module not found

### Exams
- Scheduling conflict
- Room unavailable
- Invalid date
- Non-existing module

All errors must:
- Return clear messages
- Never crash the application
- Use appropriate HTTP status codes

---

# 6️⃣ Security Guidelines

- Validate all inputs server-side
- Prevent SQL injection (use ORM only)
- Escape template variables
- Protect against CSRF (especially in Django)
- Do not expose sensitive data
- Implement authentication if required

---

# 7️⃣ UI/UX Guidelines

- Keep interface simple and academic
- Use consistent navigation
- Provide feedback messages (success / error)
- Confirm before delete actions
- Make forms clear and structured

---

# 8️⃣ Code Review Guidelines

When reviewing code, the AI must check:

- Code clarity
- Architecture consistency
- Proper database relationships
- Validation completeness
- Security risks
- Performance issues
- Redundant logic
- Naming conventions

The AI should suggest improvements but avoid unnecessary refactoring.

---

# 9️⃣ Additional Features (If Requested)

If the user asks for improvements, AI may suggest:

- Authentication & role-based access
- REST API
- Dashboard statistics
- Pagination
- Search filters
- Export to PDF/Excel
- Logging system
- Unit tests

---

# 🔟 What AI Must Avoid

- Mixing business logic inside templates
- Writing raw SQL when ORM is available
- Creating overly complex abstractions
- Ignoring validation
- Hardcoding data
- Breaking project structure

---

# ✅ Expected Outcome

The AI should generate:

- Clean
- Structured
- Secure
- Maintainable
- Academic-level professional code

This instruction file defines the mandatory coding and architectural standards for the LUS RSIS Management Application.