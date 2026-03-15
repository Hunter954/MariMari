from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import func
from app.extensions.db import db
from app.models.bonus_item import BonusItem
from app.models.comment import Comment
from app.models.episode import Episode
from app.models.extra_content import ExtraContent
from app.models.notification import Notification
from app.models.season import Season
from app.models.user import User
from app.services.auth_service import hash_password
from app.utils.decorators import admin_required
from app.utils.slug import slugify


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'users': User.query.count(),
        'seasons': Season.query.count(),
        'episodes': Episode.query.count(),
        'comments': Comment.query.count(),
    }
    recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(6).all()
    return render_template('admin/dashboard.html', stats=stats, recent_comments=recent_comments)


@admin_bp.route('/temporadas', methods=['GET', 'POST'])
@login_required
@admin_required
def temporadas():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if title:
            season = Season(
                title=title,
                slug=slugify(title),
                description=request.form.get('description', ''),
                sort_order=int(request.form.get('sort_order', 0) or 0),
                status=request.form.get('status', 'draft'),
                is_current=bool(request.form.get('is_current')),
            )
            if season.is_current:
                Season.query.update({'is_current': False})
            db.session.add(season)
            db.session.commit()
            flash('Temporada criada.', 'success')
            return redirect(url_for('admin.temporadas'))
    items = Season.query.order_by(Season.sort_order.asc()).all()
    return render_template('admin/temporadas.html', items=items)


@admin_bp.route('/episodios', methods=['GET', 'POST'])
@login_required
@admin_required
def episodios():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        season_id = request.form.get('season_id')
        if title and season_id:
            episode = Episode(
                season_id=int(season_id),
                title=title,
                slug=slugify(title),
                description=request.form.get('description', ''),
                duration_seconds=int(request.form.get('duration_seconds', 0) or 0),
                sort_order=int(request.form.get('sort_order', 0) or 0),
                status=request.form.get('status', 'draft'),
                video_url=request.form.get('video_url', ''),
                thumb_url=request.form.get('thumb_url', ''),
            )
            db.session.add(episode)
            db.session.commit()
            flash('Episódio criado.', 'success')
            return redirect(url_for('admin.episodios'))
    items = Episode.query.order_by(Episode.created_at.desc()).all()
    seasons = Season.query.order_by(Season.sort_order.asc()).all()
    return render_template('admin/episodios.html', items=items, seasons=seasons)


@admin_bp.route('/bonus', methods=['GET', 'POST'])
@login_required
@admin_required
def bonus():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if title:
            item = BonusItem(
                title=title,
                slug=slugify(title),
                description=request.form.get('description', ''),
                price_text=request.form.get('price_text', ''),
                cta_label=request.form.get('cta_label', 'Quero saber mais'),
                cta_url=request.form.get('cta_url', ''),
                image_url=request.form.get('image_url', ''),
            )
            db.session.add(item)
            db.session.commit()
            flash('Oferta bônus criada.', 'success')
            return redirect(url_for('admin.bonus'))
    items = BonusItem.query.order_by(BonusItem.created_at.desc()).all()
    return render_template('admin/bonus.html', items=items)


@admin_bp.route('/extras', methods=['GET', 'POST'])
@login_required
@admin_required
def extras():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if title:
            item = ExtraContent(
                title=title,
                slug=slugify(title),
                description=request.form.get('description', ''),
                type=request.form.get('type', 'video'),
                media_url=request.form.get('media_url', ''),
                thumb_url=request.form.get('thumb_url', ''),
            )
            db.session.add(item)
            db.session.commit()
            flash('Extra criado.', 'success')
            return redirect(url_for('admin.extras'))
    items = ExtraContent.query.order_by(ExtraContent.created_at.desc()).all()
    return render_template('admin/extras.html', items=items)


@admin_bp.route('/usuarios', methods=['GET', 'POST'])
@login_required
@admin_required
def usuarios():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        if name and email and password:
            user = User(
                name=name,
                email=email,
                password_hash=hash_password(password),
                role=request.form.get('role', 'viewer'),
                username=email.split('@')[0],
            )
            db.session.add(user)
            db.session.commit()
            flash('Usuário criado.', 'success')
            return redirect(url_for('admin.usuarios'))
    items = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/usuarios.html', items=items)


@admin_bp.route('/comentarios')
@login_required
@admin_required
def comentarios():
    items = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin/comentarios.html', items=items)


@admin_bp.route('/notificacoes', methods=['GET', 'POST'])
@login_required
@admin_required
def notificacoes():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        body = request.form.get('body', '').strip()
        if title and body:
            user_id = int(request.form.get('user_id'))
            item = Notification(user_id=user_id, title=title, body=body, link=request.form.get('link', ''))
            db.session.add(item)
            db.session.commit()
            flash('Notificação enviada.', 'success')
            return redirect(url_for('admin.notificacoes'))
    items = Notification.query.order_by(Notification.created_at.desc()).all()
    users = User.query.order_by(User.name.asc()).all()
    return render_template('admin/notificacoes.html', items=items, users=users)
