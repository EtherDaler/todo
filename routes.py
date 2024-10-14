from flask import render_template, request, redirect, url_for, Blueprint, jsonify, flash, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, decode_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from .db import db
from .models import Task, User
from .decorator import jwt_required_redirect

bp = Blueprint('main', __name__)
jwt = JWTManager()

@bp.route('/')
@jwt_required_redirect
def index():
    todos = Task.query.all()
    return render_template('index.html', todos=todos)

@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
@jwt_required_redirect
def manage_todo(todo_id=None):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')

        if todo_id:
            todo = Task.query.get(todo_id)
            todo.title = title
            todo.description = description
        else:
            todo = Task(title=title, description=description)
            db.session.add(todo)

        db.session.commit()
        return redirect(url_for('main.index'))

    todo = Task.query.get(todo_id) if todo_id else None
    return render_template('manage_todo.html', todo=todo)

@bp.route('/delete/<int:todo_id>', methods=['POST'])
@jwt_required_redirect
def delete_todo(todo_id):
    todo = Task.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            flash("Имя пользователя уже существует.")
            return redirect(url_for('auth.register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Пользователь успешно зарегистрирован.")
        return redirect(url_for('main.login'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=username)
            resp = make_response(redirect(url_for('main.index')))  # Редирект на главную страницу
            resp.set_cookie('access_token', access_token)
            return resp  # Замените на нужный маршрут

        flash("Неверное имя пользователя или пароль.")
        return redirect(url_for('main.login'))

    return render_template('login.html')
