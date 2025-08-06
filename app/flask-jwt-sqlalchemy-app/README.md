# Flask JWT SQLAlchemy App

This project is a Flask application that implements JWT-based authentication using SQLAlchemy with a SQLite database. It provides a simple API for user registration, login, and token management.

## Project Structure

```
flask-jwt-sqlalchemy-app
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── auth.py
│   ├── schemas.py
│   └── config.py
├── migrations
│   └── README.md
├── tests
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_routes.py
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-jwt-sqlalchemy-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///your_database.db
   ```

5. **Run database migrations:**
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the application:**
   ```
   python run.py
   ```

## Usage

- **Register a new user:**
  POST `/auth/register`
  
- **Login:**
  POST `/auth/login`

- **Access protected routes:**
  Use the JWT token received upon login in the Authorization header as `Bearer <token>`.

## Testing

To run the tests, use:
```
pytest
```

## License

This project is licensed under the MIT License.