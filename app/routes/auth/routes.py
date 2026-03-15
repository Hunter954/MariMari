from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.extensions.db import db
from app.models.user import User
from app.services.auth_service import check_password, hash_password


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('platform.home'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password(user.password_hash, password):
            login_user(user, remember=True)
            return redirect(url_for('platform.home'))
        flash('Email ou senha inválidos.', 'error')
    return render_template('auth/login.html')


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('platform.home'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not name or not email or len(password) < 6:
            flash('Preencha nome, email e uma senha com pelo menos 6 caracteres.', 'error')
            return render_template('auth/cadastro.html')
        if User.query.filter_by(email=email).first():
            flash('Já existe uma conta com esse email.', 'error')
            return render_template('auth/cadastro.html')
        user = User(name=name, email=email, password_hash=hash_password(password), username=email.split('@')[0])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Conta criada com sucesso.', 'success')
        return redirect(url_for('platform.meus_dados'))
    return render_template('auth/cadastro.html')


@auth_bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        flash('Fluxo de recuperação preparado. Conecte seu provedor de email para ativar o envio real.', 'info')
    return render_template('auth/recuperar_senha.html')


@auth_bp.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    if request.method == 'POST':
        flash('Fluxo de redefinição preparado para integração com token assinado.', 'info')
    return render_template('auth/redefinir_senha.html', token=token)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da plataforma.', 'info')
    return redirect(url_for('auth.login'))
