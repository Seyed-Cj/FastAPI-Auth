# FastAPI Authentication API

A full-featured authentication API built with **FastAPI**, **SQLAlchemy**, **JWT**, and **Passlib**. Supports user registration, login, token-based authentication, and protected routes.

## Features
- User registration with hashed passwords
- Login with email & password
- JWT access and refresh tokens
- Protected endpoints requiring authentication
- Password hashing with bcrypt
- Simple SQLAlchemy-based database integration

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Seyed-Cj/TelegramBot-FastAPI-Panel.git
cd FastAPI-Auth
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in .env:
```bash
SECRET_KEY=123456
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=fastapi_auth
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints
1. Register

- POST /auth/register

* Request (JSON):

```json
{
  "user_name": "seyed",
  "email": "seyed@example.com",
  "password": "securepassword"
}
```

2. Login

- POST /auth/login

* Request (JSON):

```json
{
  "email": "seyed@example.com",
  "password": "securepassword"
}
```

3. Refresh Access Token

- POST /auth/refresh

* Request (JSON):

```json
{
  "refresh_token": "jwt_refresh_token"
}
```

## Security Notes

- Passwords are bcrypt-hashed and never stored in plaintext.
- Tokens are JWT-based with expiry.
- Always protect .env secrets.
- Truncate passwords manually if longer than 72 bytes due to bcrypt limitation.