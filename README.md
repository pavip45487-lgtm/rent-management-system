# Home Rent Management System

A production-ready Home Rent Management System built with Flask, SQLite, SQLAlchemy, Flask-Login, and Flask-WTF.

## Features

- User registration and login
- Password hashing and reset via token
- Add / edit / delete properties with multiple image uploads
- Property listing, search, filters, pagination
- Wishlist management
- Contact owner (simulated)
- Responsive Bootstrap 5 UI with cards and gallery

## Setup

1. Create a virtual environment and activate it:

```bash
python -m venv venv
venv\\Scripts\\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

The application will create `database.db` and the uploads folder on first run.

## Notes

- For production, set `SECRET_KEY` and `DATABASE_URL` environment variables.
- Email sending for password reset is simulated by displaying the reset link in flash messages.
