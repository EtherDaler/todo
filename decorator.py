import os

from functools import wraps
from flask import request, redirect, url_for, flash
from jwt import decode, InvalidTokenError, ExpiredSignatureError
from flask_jwt_extended import JWTManager

# Настраиваем JWTManager
jwt = JWTManager()

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTcyODg3OTg1MCwiaWF0IjoxNzI4ODc5ODUwfQ.GduLPSumdCt7Ws6sY81W4h4fMVt_TXeLV7I0Exe-a-k')

def jwt_required_redirect(f):
    """Декоратор для проверки JWT и перенаправления на страницу регистрации."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('access_token')  # Получаем токен из cookies
        if not token:
            flash('Пожалуйста, авторизуйтесь.')
            return redirect(url_for('main.login'))  # Перенаправляем на страницу авторизации

        try:
            # Декодируем токен
            decoded_token = decode(token, SECRET_KEY, algorithms=['HS256'])
            user_identity = decoded_token.get('sub')
            print(user_identity)
            return f(*args, **kwargs)

        except ExpiredSignatureError:
            flash('Срок действия токена истек, пожалуйста, авторизуйтесь снова.')
            return redirect(url_for('main.login'))  # Перенаправляем на авторизацию

        except InvalidTokenError:
            flash('Неверный токен, пожалуйста, авторизуйтесь.')
            return redirect(url_for('main.login'))  # Перенаправляем на авторизацию

    return decorated_function