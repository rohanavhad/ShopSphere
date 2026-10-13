import os
os.environ["DATABASE_URL"] = "sqlite:///./test_ecommerce.db"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import engine
from app.db.base import Base, load_models

@pytest.fixture()
def client():
    load_models()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
