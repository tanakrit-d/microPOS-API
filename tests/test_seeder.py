from decimal import Decimal
from uuid import UUID

import pytest
from pydantic import ValidationError

from supabase import AClient
from utils.exceptions import ItemSeedingError, ValidationSeedingError
from utils.seeder import DataSeeder


@pytest.fixture
async def seeder(mocker):
    mock_client = mocker.AsyncMock(spec=AClient)
    return DataSeeder(mock_client)


@pytest.mark.asyncio
async def test_generate_fake_item_success(seeder) -> None:
    """Test that generated fake items meet all schema requirements."""
    fake_item = seeder.generate_fake_item()

    assert len(fake_item.title) <= 22
    assert isinstance(fake_item.price, Decimal)
    assert fake_item.price >= Decimal("0.00")
    assert len(str(fake_item.price).split(".")[-1]) <= 2  # Check decimal places
    assert isinstance(fake_item.is_available, bool)
    assert fake_item.title_full is not None
    assert fake_item.description is not None
    assert fake_item.categories is not None
    assert len(fake_item.categories) >= 1
    assert all(isinstance(cat, UUID) for cat in fake_item.categories)


@pytest.mark.asyncio
async def test_generate_fake_item_validation_error(seeder, mocker) -> None:
    """Test handling of validation errors during item generation."""
    # Mock Faker to generate an invalid price
    mocker.patch("faker.Faker.pyfloat", return_value=-1.0)

    with pytest.raises(ValidationSeedingError) as exc_info:
        seeder.generate_fake_item()

    assert "price" in str(exc_info.value)
    assert exc_info.value.details["field_name"] == "price"


@pytest.mark.asyncio
async def test_seed_items_success(seeder, mocker) -> None:
    """Test successful seeding of items."""
    # Mock the insert execution
    mock_response = mocker.AsyncMock()
    mock_response.data = [{"title": "Test Item", "id": "123"}]
    seeder.client.table.return_value.insert.return_value.execute.return_value = mock_response

    await seeder.seed_items(count=5)

    assert seeder.client.table.call_count == 5
    assert seeder.client.table().insert.call_count == 5


@pytest.mark.asyncio
async def test_seed_items_partial_failure(seeder, mocker) -> None:
    """Test handling of partial failures during seeding."""
    # Mock successful insertions for some items and failures for others
    mock_success = mocker.AsyncMock()
    mock_success.data = [{"title": "Test Item", "id": "123"}]

    def side_effect(*args, **kwargs):
        if seeder.client.table.call_count % 2 == 0:
            msg = "Database error"
            raise Exception(msg)
        return mock_success

    seeder.client.table.return_value.insert.return_value.execute.side_effect = side_effect

    with pytest.raises(ItemSeedingError) as exc_info:
        await seeder.seed_items(count=4)

    assert "Seeding completed with errors" in str(exc_info.value)
    assert exc_info.value.details["errors"]
    assert len(exc_info.value.details["errors"]) == 2  # Two failures


@pytest.mark.asyncio
async def test_seed_items_complete_failure(seeder, mocker):
    """Test handling of complete failure during seeding."""
    # Mock database error
    seeder.client.table.return_value.insert.return_value.execute.side_effect = \
        Exception("Database connection failed")

    with pytest.raises(ItemSeedingError) as exc_info:
        await seeder.seed_items(count=3)

    assert "Seeding completed with errors" in str(exc_info.value)
    assert exc_info.value.details["errors"]
    assert len(exc_info.value.details["errors"]) == 3  # All attempts failed
