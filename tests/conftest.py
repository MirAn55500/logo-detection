import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from app import create_app


@pytest.fixture
async def client(aiohttp_client):
    app = create_app()
    return await aiohttp_client(app)
