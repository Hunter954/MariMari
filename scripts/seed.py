from datetime import datetime, timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app
from app.extensions.db import db
from app.models.bonus_item import BonusItem
from app.models.episode import Episode
from app.models.extra_content import ExtraContent
from app.models.notification import Notification
from app.models.season import Season
from app.models.subscription import Subscription
from app.models.user import User
from app.services.auth_service import hash_password
from app.utils.slug import slugify

app = create_app()

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email='admin@mariolivier.com').first()
    if not admin:
        admin = User(name='Kevin Premoli', email='admin@mariolivier.com', password_hash=hash_password('12345678'), role='admin', username='kevin')
        db.session.add(admin)

    user = User.query.filter_by(email='cliente@mariolivier.com').first()
    if not user:
        user = User(name='Kevin Premoli', email='cliente@mariolivier.com', password_hash=hash_password('12345678'), role='viewer', username='kevinpremoli')
        db.session.add(user)
    db.session.commit()

    if Season.query.count() == 0:
        seasons = []
        for idx in range(1, 7):
            season = Season(
                title=f'Temporada {idx}',
                slug=f'temporada-{idx}',
                description=f'Uma nova fase do reality com estética premium e histórias mais íntimas. Temporada {idx}.',
                sort_order=idx,
                status='published',
                is_current=idx == 1,
                release_date=datetime.utcnow() + timedelta(days=idx * 7),
            )
            db.session.add(season)
            seasons.append(season)
        db.session.commit()

        for idx in range(1, 6):
            episode = Episode(
                season_id=seasons[0].id,
                title=f'Episódio {idx}',
                slug=f'temporada-1-episodio-{idx}',
                description='Episódio com narrativa cinematográfica, retomada automática e comentários em tempo real.',
                duration_seconds=2460,
                sort_order=idx,
                status='published',
                release_date=datetime.utcnow() + timedelta(days=idx),
                is_featured=idx == 1,
                video_url='/media/videos/temporada-1-episodio-1.mp4',
                thumb_url='/media/thumbs/temporada-1-episodio-1.jpg',
            )
            db.session.add(episode)

        db.session.add_all([
            BonusItem(title='Visita especial na sua loja', slug='visita-especial-loja', description='Ativação exclusiva com presença da influencer para campanha presencial.', price_text='Sob consulta', cta_label='Solicitar proposta', cta_url='#'),
            BonusItem(title='Pacote de stories patrocinados', slug='stories-patrocinados', description='Entrega de stories com linguagem da criadora e CTA comercial.', price_text='A partir de R$ 2.900', cta_label='Quero contratar', cta_url='#'),
        ])
        db.session.add_all([
            ExtraContent(title='Making of do episódio 1', slug='making-of-ep-1', description='Bastidores da gravação com cenas inéditas.', type='video'),
            ExtraContent(title='Galeria exclusiva do set', slug='galeria-set', description='Fotos premium e referências de arte.', type='gallery'),
        ])
        db.session.commit()

    if Notification.query.count() == 0:
        db.session.add_all([
            Notification(user_id=user.id, title='Novo episódio disponível', body='O episódio 2 já está liberado na plataforma.', link='/episodio/temporada-1-episodio-2'),
            Notification(user_id=user.id, title='Oferta especial no bônus', body='Uma nova ativação comercial foi adicionada na área bônus.', link='/bonus'),
        ])
        db.session.add(Subscription(user_id=user.id, plan_name='Premium Anual', status='active', provider='manual'))
        db.session.commit()

    print('Seed concluído com sucesso.')
