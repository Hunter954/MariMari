from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.extensions.db import db
from app.models.comment import Comment
from app.models.episode import Episode
from app.services.bonus_service import register_interest
from app.services.comment_service import create_comment, toggle_comment_like
from app.services.notification_service import mark_notification_read
from app.services.video_service import save_progress, toggle_video_like


api_bp = Blueprint('api', __name__)


@api_bp.post('/player/progress')
@login_required
def player_progress():
    payload = request.get_json(force=True)
    episode = Episode.query.get_or_404(int(payload.get('episode_id')))
    record = save_progress(current_user.id, episode.id, int(payload.get('progress_seconds', 0)), episode.duration_seconds)
    return jsonify({'ok': True, 'completed': record.completed, 'progress_seconds': record.progress_seconds})


@api_bp.post('/player/like')
@login_required
def player_like():
    payload = request.get_json(force=True)
    episode_id = int(payload.get('episode_id'))
    active = toggle_video_like(current_user.id, episode_id)
    return jsonify({'ok': True, 'liked': active})


@api_bp.post('/comments/create')
@login_required
def comments_create():
    payload = request.get_json(force=True)
    content = (payload.get('content') or '').strip()
    if not content:
        return jsonify({'ok': False, 'message': 'Comentário vazio.'}), 400
    comment = create_comment(current_user.id, int(payload.get('episode_id')), content)
    return jsonify({'ok': True, 'comment': {
        'id': comment.id,
        'author': current_user.name,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%d/%m/%Y %H:%M'),
    }})


@api_bp.post('/comments/<int:comment_id>/like')
@login_required
def comments_like(comment_id):
    liked = toggle_comment_like(current_user.id, comment_id)
    return jsonify({'ok': True, 'liked': liked})


@api_bp.post('/comments/<int:comment_id>/delete')
@login_required
def comments_delete(comment_id):
    comment = Comment.query.filter_by(id=comment_id, user_id=current_user.id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'ok': True})


@api_bp.post('/notifications/read')
@login_required
def notifications_read():
    payload = request.get_json(force=True)
    item = mark_notification_read(int(payload.get('notification_id')), current_user.id)
    return jsonify({'ok': True, 'notification_id': item.id})


@api_bp.post('/bonus/interest')
@login_required
def bonus_interest():
    payload = request.get_json(force=True)
    lead = register_interest(current_user.id, int(payload.get('bonus_item_id')), payload.get('message', ''))
    return jsonify({'ok': True, 'lead_id': lead.id})
