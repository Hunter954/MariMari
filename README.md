# Mari Olivier MVP

MVP fullstack em Flask + PostgreSQL + Railway Volume.

## O que já vem pronto
- autenticação com Flask-Login
- shell premium desktop-first
- home, temporadas, detalhe da temporada, episódio, bônus, extras, assinatura, meus dados e notificações
- painel admin para temporadas, episódios, bônus, extras, usuários, comentários e notificações
- API interna para progresso do player, likes, comentários, notificações e leads de bônus
- modelos SQLAlchemy preparados para PostgreSQL
- seed inicial com dados demo
- scripts para criar admin
- estrutura pronta para Railway + Postgres + Volume

## Como rodar local
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
flask --app wsgi:app db init
flask --app wsgi:app db migrate -m "init"
flask --app wsgi:app db upgrade
python scripts/seed.py
python scripts/create_admin.py
flask --app wsgi:app run
```

## Railway
1. Suba o projeto no GitHub.
2. Crie um projeto no Railway e conecte o repositório.
3. Adicione um serviço PostgreSQL.
4. Adicione um Volume e monte em `/app/storage`.
5. Defina as variáveis do `.env.example`.
6. No primeiro deploy, rode:
   - `flask --app wsgi:app db init` (apenas uma vez se ainda não existir migrations)
   - `flask --app wsgi:app db migrate -m "init"`
   - `flask --app wsgi:app db upgrade`
   - `python scripts/seed.py`

## Observação
Para acelerar a entrega, o app já está funcional com renderização server-side. Ele está pronto para receber vídeos reais, thumbnails e assets no volume do Railway.
