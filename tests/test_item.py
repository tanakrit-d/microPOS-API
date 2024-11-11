import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from supabase import AClient, PostgrestAPIResponse

from src.api.item.router import router as item_routes
from src.api.item.schemas import Item, ItemResponseModel
from src.database import lifespan

# Test data
SAMPLE_UUID = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
SAMPLE_CATEGORY_UUID = uuid.UUID("123e4567-e89b-12d3-a456-426614174001")
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_UNPROCESSABLE = 422
HTTP_INTERNAL_ERROR = 500

SAMPLE_ITEM = {
    "id": str(SAMPLE_UUID),
    "title": "Mystery Curry",
    "title_full": "Mysterious Curry with vegetables",
    "description": "Mystery Curry from another planet!",
    "categories": [str(SAMPLE_CATEGORY_UUID)],
    "price": "12.50",
    "image_uri": "https://www.example.com/mystery_curry.png",
    "created_at": "2023-10-24T12:00:00Z",
    "updated_at": "2023-10-25T12:00:00Z",
    "is_available": True,
}


@pytest.fixture
def app() -> FastAPI:
    """Create a test FastAPI application."""
    app = FastAPI()
    app.include_router(item_routes)
    return app


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def mock_supabase_client() -> AsyncGenerator[MagicMock, None]:
    """Create a mock Supabase client."""
    with patch("src.database.get_supabase_client") as mock:
        client = AsyncMock(spec=AClient)
        mock.return_value = client
        yield client


@pytest.mark.anyio
async def test_get_item_success(client: TestClient, mock_supabase_client: AsyncMock) -> None:
    """Test successful retrieval of a single item."""
    # Mock the Supabase response
    mock_response = PostgrestAPIResponse(
        data=[SAMPLE_ITEM],
        count=1,
    )
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Make the request
    response = client.get(f"/item/{SAMPLE_UUID}")

    # Verify the response
    assert response.status_code == HTTP_OK
    assert response.json()["data"][0]["id"] == str(SAMPLE_UUID)
    assert response.json()["count"] == 1


@pytest.mark.anyio
async def test_get_item_not_found(client: TestClient, mock_supabase_client: AsyncMock) -> None:
    """Test retrieval of non-existent item."""
    # Mock empty response
    mock_response = PostgrestAPIResponse(data=[], count=0)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    response = client.get(f"/item/{SAMPLE_UUID}")
    assert response.status_code == HTTP_OK
    assert response.json()["data"] == []
    assert response.json()["count"] == 0


@pytest.mark.anyio
async def test_get_items_success(client: TestClient, mock_supabase_client: AsyncMock) -> None:
    """Test successful retrieval of all items."""
    mock_response = PostgrestAPIResponse(
        data=[SAMPLE_ITEM],
        count=1,
    )
    mock_supabase_client.table.return_value.select.return_value.execute.return_value = mock_response

    response = client.get("/item/")
    assert response.status_code == HTTP_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["count"] == 1


@pytest.mark.anyio
async def test_get_items_with_availability_filter(client: TestClient, mock_supabase_client: AsyncMock) -> None:
    """Test retrieval of items filtered by availability."""
    mock_response = PostgrestAPIResponse(
        data=[SAMPLE_ITEM],
        count=1,
    )
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    response = client.get("/item/?available=true")
    assert response.status_code == HTTP_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["is_available"] is True


@pytest.mark.anyio
async def test_create_item_success(client: TestClient, mock_supabase_client: AsyncMock) -> None:
    """Test successful creation of an item."""
    new_item = {
        "title": "New Curry",
        "price": "15.50",
        "is_available": True,
        "title_full": "New Curry with special sauce",
        "description": "A new curry creation",
        "categories": [str(SAMPLE_CATEGORY_UUID)],
        "image_uri": "https://example.com/new_curry.png",
    }

    mock_response = PostgrestAPIResponse(
        data=[{**new_item, "id": str(SAMPLE_UUID), "created_at": "2024-10-26T12:00:00Z"}],
        count=1,
    )
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = mock_response

    response = client.post("/item/create", json=new_item)
    print(response)
    assert response.status_code == HTTP_CREATED
    assert response.json()["data"][0]["title"] == "New Curry"


@pytest.mark.anyio
async def test_create_item_validation_error(client: TestClient) -> None:
    """Test item creation with invalid data."""
    invalid_item = {
        "title": "New Curry",
        "price": "-15.50",  # Invalid negative price
        "is_available": True,
    }

    response = client.post("/item/create", json=invalid_item)
    assert response.status_code == HTTP_UNPROCESSABLE


@pytest.mark.anyio
async def test_update_item_success(client: TestClient, mock_supabase_client: AsyncMock) -> None:
    """Test successful update of an item."""
    update_data = {"title": "Updated Curry", "price": "18.50", "is_available": False}

    mock_response = PostgrestAPIResponse(
        data=[{**SAMPLE_ITEM, **update_data, "updated_at": "2024-10-26T12:00:00Z"}],
        count=1,
    )
    mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response

    response = client.patch(f"/item/{SAMPLE_UUID}", json=update_data)
    assert response.status_code == HTTP_OK
    assert response.json()["data"][0]["title"] == "Updated Curry"
    assert response.json()["data"][0]["price"] == "18.50"


@pytest.mark.anyio
async def test_delete_item_success(client: TestClient, mock_supabase_client: AsyncMock) -> None:
    """Test successful deletion of an item."""
    mock_response = PostgrestAPIResponse(
        data=[SAMPLE_ITEM],
        count=1,
    )
    mock_supabase_client.table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_response

    response = client.delete(f"/item/{SAMPLE_UUID}")
    assert response.status_code == HTTP_OK
    assert response.json()["data"][0]["id"] == str(SAMPLE_UUID)


@pytest.mark.anyio
async def test_supabase_error_handling(client: TestClient, mock_supabase_client: AsyncMock) -> None:
    """Test error handling when Supabase operations fail."""
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")

    response = client.get(f"/item/{SAMPLE_UUID}")
    assert response.status_code == HTTP_INTERNAL_ERROR
    assert "Error ID" in response.json()["detail"]
