from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from app.extensions.db import db
from app.models.bonus_item import BonusItem
from app.models.comment import Comment
from app.models.episode import Episode
from app.models.extra_content import ExtraContent
from app.models.notification import Notification
from app.models.season import Season
from app.models.subscription import Subscription
from app.models.user import User
from app.models.video_like import VideoLike
from app.models.watch_progress import WatchProgress
from app.utils.dates import format_dt


platform_bp = Blueprint('platform', __name__)


def _progress_lookup(user_id: int):
    rows = WatchProgress.query.filter_by(user_id=user_id).all()
    return {row.episode_id: row for row in rows}


@platform_bp.app_template_filter('duration_label')
def duration_label(seconds):
    total_minutes = max(int((seconds or 0) / 60), 1)
    return f'{total_minutes}min'


@platform_bp.app_template_filter('format_dt')
def template_format_dt(value):
    return format_dt(value)


@platform_bp.route('/')
@login_required
def home():
    current_season = Season.query.filter_by(is_current=True).first() or Season.query.order_by(Season.sort_order.asc()).first()
    next_episodes = Episode.query.filter(Episode.status == 'published').order_by(Episode.release_date.asc().nullslast()).limit(4).all()
    upcoming_seasons = Season.query.order_by(Season.sort_order.asc()).limit(5).all()
    progress_map = _progress_lookup(current_user.id)
    featured = None
    featured_progress = None
    if current_season and current_season.episodes:
        featured = current_season.episodes[0]
        featured_progress = progress_map.get(featured.id)
    unread_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('platform/home.html', current_season=current_season, next_episodes=next_episodes,
                           upcoming_seasons=upcoming_seasons, featured=featured, featured_progress=featured_progress,
                           unread_notifications=unread_notifications)


@platform_bp.route('/temporadas')
@login_required
def temporadas():
    seasons = Season.query.order_by(Season.sort_order.asc()).all()
    return render_template('platform/temporadas.html', seasons=seasons)


@platform_bp.route('/temporadas/<slug>')
@login_required
def temporada_detalhe(slug):
    season = Season.query.filter_by(slug=slug).first_or_404()
    progress_map = _progress_lookup(current_user.id)
    return render_template('platform/temporada_detalhe.html', season=season, progress_map=progress_map)


@platform_bp.route('/episodio/<slug>')
@login_required
def episodio(slug):
    episode = Episode.query.filter_by(slug=slug).first_or_404()
    comments = Comment.query.filter_by(episode_id=episode.id, is_hidden=False).order_by(Comment.created_at.desc()).all()
    progress = WatchProgress.query.filter_by(user_id=current_user.id, episode_id=episode.id).first()
    liked = VideoLike.query.filter_by(user_id=current_user.id, episode_id=episode.id).first() is not None
    likes_count = VideoLike.query.filter_by(episode_id=episode.id).count()
    related = Episode.query.filter(Episode.season_id == episode.season_id, Episode.id != episode.id).order_by(Episode.sort_order.asc()).limit(4).all()
    return render_template('platform/episodio.html', episode=episode, comments=comments, progress=progress,
                           liked=liked, likes_count=likes_count, related=related)


@platform_bp.route('/bonus')
@login_required
def bonus():
    items = BonusItem.query.filter_by(is_active=True).order_by(BonusItem.created_at.desc()).all()
    return render_template('platform/bonus.html', items=items)


@platform_bp.route('/extras')
@login_required
def extras():
    items = ExtraContent.query.filter_by(is_published=True).order_by(ExtraContent.created_at.desc()).all()
    return render_template('platform/extras.html', items=items)


@platform_bp.route('/assinatura')
@login_required
def assinatura():
    subscription = Subscription.query.filter_by(user_id=current_user.id).order_by(Subscription.created_at.desc()).first()
    return render_template('platform/assinatura.html', subscription=subscription)


@platform_bp.route('/meus-dados', methods=['GET', 'POST'])
@login_required
def meus_dados():
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.city = request.form.get('city', current_user.city)
        current_user.state = request.form.get('state', current_user.state)
        current_user.username = request.form.get('username', current_user.username)
        db.session.commit()
        flash('Dados atualizados com sucesso.', 'success')
        return redirect(url_for('platform.meus_dados'))
    return render_template('platform/meus_dados.html')


@platform_bp.route('/notificacoes')
@login_required
def notificacoes():
    items = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('platform/notificacoes.html', items=items)
