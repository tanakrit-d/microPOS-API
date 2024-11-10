from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from json.decoder import JSONDecodeError
from typing import Any

from faker import Faker
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from src.api.item.schemas import ItemCreate
from src.database import create_supabase
from supabase import AClient
from utils.exceptions import ItemSeedingError, ValidationSeedingError
from utils.logger import logger

fake = Faker()

class DataSeeder:
    """Utility class for seeding test data into the database."""

    def __init__(self, client: AClient) -> None:
        self.client = client
        self.categories = [
            "Appetizers",
            "Main Course",
            "Desserts",
            "Beverages",
            "Specials",
        ]
        self.food_adjectives = [
            "Spicy", "Fresh", "Grilled", "Homemade", "Traditional",
            "Seasonal", "Organic", "Local", "House Special", "Chef's",
        ]
        self.food_types = [
            "Curry", "Stir-fry", "Salad", "Soup", "Rice Bowl",
            "Noodles", "Sandwich", "Pizza", "Pasta", "Seafood",
        ]

    def generate_fake_item(self) -> ItemCreate:
        """
        Generate a single fake menu item.

        Raises:
            ValidationSeedingError: If generated data fails validation
            ItemSeedingError: If there's an error during item generation

        """
        try:
            adjective = fake.random_element(self.food_adjectives)
            food_type = fake.random_element(self.food_types)

            title = f"{adjective} {food_type}"
            title = title[:22]

            try:
                price = Decimal(str(fake.pyfloat(
                    min_value=5.0,
                    max_value=35.0,
                    right_digits=2,
                ))).quantize(Decimal("0.01"))
            except (InvalidOperation, ValueError) as e:
                raise ValidationSeedingError(
                    field_name="price",
                    invalid_value=price,
                    validation_error=e,
                ) from e

            item_data = {
                "title": title,
                "title_full": f"{adjective} {food_type} with {fake.word()} {fake.word()}",
                "description": fake.sentence(nb_words=10),
                "price": price,
                "is_available": fake.boolean(chance_of_getting_true=80),
                "image_uri": f"https://example.com/images/{uuid.uuid4()}.jpg",
                "created_at": datetime.now(UTC),
                "categories": [uuid.uuid4() for _ in range(fake.random_int(min=1, max=3))],
            }

            return ItemCreate(**item_data)

        except ValidationError as e:
            raise ValidationSeedingError(
                field_name=e.errors()[0]["loc"][0],
                invalid_value=e.errors()[0]["input"],
                validation_error=e,
            ) from e
        except Exception as e:
            raise ItemSeedingError(
                message="Failed to generate fake item",
                original_error=e,
            ) from e

    async def seed_items(self, count: int = 10) -> None:
            """
            Seed the specified number of fake items into the database.

            Args:
                count: Number of items to seed

            Raises:
                ItemSeedingError: If seeding fails for any reason

            """
            logger.info(f"Seeding {count} fake menu items...")

            seeded_count = 0
            errors = []

            for i in range(count):
                try:
                    fake_item = self.generate_fake_item()
                    item_dict = fake_item.model_dump()
                    item_json_encoded = jsonable_encoder(item_dict)

                    response = await self.client.table("item").insert(item_json_encoded).execute()

                    logger.info(
                        "Created fake item: title=%s; id=%s",
                        response.data[0]["title"],
                        response.data[0]["id"],
                    )
                    seeded_count += 1

                except ItemSeedingError as e:
                    logger.error(f"Failed to seed item {i+1}/{count}: {e!s}")
                    errors.append(e)
                except (ValidationError, JSONDecodeError) as e:
                    error = ItemSeedingError(
                        message=f"Data validation error for item {i+1}/{count}",
                        original_error=e,
                    )
                    logger.error(str(error))
                    errors.append(error)
                except (ValueError, TypeError) as e:
                    error = ItemSeedingError(
                        message=f"Data type error while seeding item {i+1}/{count}",
                        original_error=e,
                    )
                    logger.error(str(error))
                    errors.append(error)

            if errors:
                raise ItemSeedingError(
                    message=f"Seeding completed with errors. Successfully seeded {seeded_count}/{count} items.",
                    details={"errors": [{"error_id": e.error_id, "details": e.details} for e in errors]},
                )

            logger.info(f"Successfully seeded {seeded_count} items")

async def main(items: int = 1) -> None:
    """Run the seeding function."""
    client = await create_supabase()
    seeder = DataSeeder(client)

    try:
        await seeder.seed_items(items)
    except ItemSeedingError as e:
        logger.error(f"Seeding failed: {e!s}")
        logger.error(f"Error details: {e.details}")
    finally:
        await client.auth.sign_out()
