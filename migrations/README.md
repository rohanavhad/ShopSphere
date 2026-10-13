# Database migrations

Alembic migration files belong in this directory. To initialize Alembic after installing dependencies:

```bash
alembic init migrations
```

Configure `sqlalchemy.url` in `alembic.ini` (or use an environment-aware `env.py`) and import `Base` metadata from `app.db.base`. Generate revisions with `alembic revision --autogenerate -m "describe schema"` and apply with `alembic upgrade head`.

The app currently creates tables at startup to make local onboarding easy. Disable `Base.metadata.create_all` and use migrations as the deployment workflow in production.
