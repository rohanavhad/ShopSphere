# ShopSphere — FastAPI E-commerce Starter

A structured full-stack learning project with a FastAPI REST API, SQLAlchemy ORM, SQLite by default, JWT authentication, product catalog, cart UI, order placement, and tests.

## Features

- Register, sign in, and retrieve the current user using JWT bearer tokens.
- Browse/search products with pagination.
- Add products through the API (currently a demo endpoint; protect it with an admin role before production).
- Browser cart persisted in local storage.
- Authenticated checkout creates an order, stores line items, and decreases inventory.
- Interactive API documentation at `/docs`.
- Unit/integration test starter suite.

## Architecture

- `api/v1/endpoints`: HTTP routing and request/response handling.
- `services`: business logic.
- `models`: SQLAlchemy database tables.
- `schemas`: Pydantic validation and response models.
- `dependencies`: reusable authentication dependencies.
- `core`: configuration, password/token security, exception handling.
- `db`: SQLAlchemy engine/session and declarative metadata.
- `frontend`: plain HTML/CSS/JS storefront.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

On macOS/Linux, use `cp .env.example .env` instead of `copy`. Set a unique `SECRET_KEY` in `.env` before using anything beyond local development.

Open:
- Storefront: http://127.0.0.1:8000
- Sign in/register: http://127.0.0.1:8000/login
- Cart: http://127.0.0.1:8000/cart
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Add sample products

Use Swagger UI at `/docs` → `POST /api/v1/products/`:

```json
{
  "name": "Everyday Backpack",
  "description": "A lightweight commuter backpack.",
  "price": "2499.00",
  "stock": 12,
  "image_url": ""
}
```

Repeat with a few products to populate the storefront. The UI uses illustrative symbols instead of remote product images.

## Main API endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Create account | No |
| POST | `/api/v1/auth/login` | Sign in | No |
| GET | `/api/v1/auth/me` | Current user | Yes |
| GET | `/api/v1/products/` | List/search products | No |
| POST | `/api/v1/products/` | Create product | Demo only; add admin authorization |
| POST | `/api/v1/orders/` | Place order | Yes |
| GET | `/api/v1/orders/` | Current user's orders | Yes |
| GET | `/health` | Health check | No |

## Run tests

```bash
pytest -q
```

Tests use a separate SQLite database file (`test_ecommerce.db`) and remove its tables between tests.

## Production hardening checklist

This is a learning starter, not a production-ready commerce platform. Before deployment:
1. Replace the development secret and load secrets from a managed secret store.
2. Add admin roles and authorization for product creation/update/deletion.
3. Use Alembic migrations instead of `create_all` during application startup.
4. Use PostgreSQL (and validate locking/transaction behavior) for concurrent checkout.
5. Add payment-provider integration, idempotency, refunds, tax/shipping, and order state transitions.
6. Add rate limiting, email verification, password reset, audit logging, structured logs, and monitoring.
7. Restrict CORS origins and enforce HTTPS.
8. Add pagination limits, inventory reservation/expiry, and stronger concurrency tests.
9. Add CI, formatting/linting, dependency scanning, and deployment configuration.

## Important implementation notes

- Passwords are hashed; plaintext passwords are never stored.
- JWT access tokens expire after a configurable interval.
- Orders are scoped to the authenticated user.
- Checkout validates product availability and stock before creating order items.
- SQLite does not implement row-level `FOR UPDATE` locking the same way PostgreSQL does. Use PostgreSQL and test transaction behavior for production workloads.
- Payment is intentionally not implemented; creating an order does not charge a customer.
