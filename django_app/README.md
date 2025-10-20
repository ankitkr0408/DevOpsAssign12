# Django Authentication App

This Django application provides a simple authentication system with login, registration, home page, and logout functionality as required for the DevOps assignment.

## Features

- **Login Page**: Users can log in with their Roll No (username) and Admission No (password)
- **Registration Page**: New users can register by providing Roll No and Admission No
- **Home Page**: After successful login, displays "Hello [username] How are you"
- **Logout**: Users can log out and return to the login page
- **Database**: Uses PostgreSQL in production and SQLite for local development

## Quick Start

### Local Development (SQLite)

1. **Setup the application:**
   ```bash
   python setup.py
   ```

2. **Or manually:**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Access the application:**
   - Login: http://127.0.0.1:8000/login/
   - Register: http://127.0.0.1:8000/register/
   - Admin: http://127.0.0.1:8000/admin/

### Production (PostgreSQL)

Set the following environment variables:
```bash
export DB_HOST=your_postgres_host
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_PORT=5432
export DEBUG=False
export ALLOWED_HOSTS=your_domain.com,your_ip_address
```

## Testing

Run the test script to verify functionality:
```bash
python test_app.py
```

## Database Schema

The application uses a simple `login` table:
- `username` (VARCHAR 50): Roll No (e.g., ITA700)
- `password` (VARCHAR 100): Admission No (e.g., 2022PE0000)
- `created_at` (TIMESTAMP): Registration timestamp

## URL Structure

- `/` → Redirects to login page
- `/login/` → Login form
- `/register/` → Registration form
- `/home/` → Authenticated home page (requires login)
- `/logout/` → Logout and redirect to login
- `/admin/` → Django admin interface

## Docker Support

This app is designed to work with Docker and Docker Swarm. The database configuration automatically switches to PostgreSQL when the `DB_HOST` environment variable is set.

## Files Structure

```
django_app/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── setup.py              # Setup script
├── test_app.py           # Test script
├── run_server.py         # Development server script
├── mysite/               # Django project settings
│   ├── settings.py       # Main settings
│   ├── urls.py          # URL routing
│   └── ...
└── accounts/             # Authentication app
    ├── models.py         # Login model
    ├── views.py          # Authentication views
    ├── urls.py           # App URL routing
    ├── admin.py          # Admin configuration
    ├── templates/        # HTML templates
    │   ├── login.html
    │   ├── register.html
    │   └── home.html
    └── migrations/       # Database migrations
```

## Notes

- The application uses Django's session framework for authentication
- Passwords are stored in plain text (simplified for assignment purposes)
- The app supports both SQLite (development) and PostgreSQL (production)
- Static files are handled by WhiteNoise for production deployment
- All forms include CSRF protection
- Error messages are displayed using Django's messages framework