from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from json.decoder import JSONDecodeError

from faker import Faker
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from src.api.item.schemas import ItemCreate
from src.config import Environment, get_config
from src.database import create_supabase
from supabase import AClient
from utils.exceptions import ItemSeedingError, ValidationSeedingError
from utils.logger import logger

fake = Faker()

class DataSeeder:
    """Utility class for seeding test data into the database."""

    def __init__(self, client: AClient) -> None:
        """
        Initialize the DataSeeder with a database client and environment-specific configurations.

        Args:
            client (AClient): The Supabase client used to interact with the database.

        Attributes:
            client (AClient): The provided database client instance.
            config: Configuration settings retrieved from `get_config`.
            environment (Environment): The current environment (e.g., local, development, production).
            categories (list[str]): List of item categories used to classify seeded data.
            food_adjectives (list[str]): Adjectives for randomizing item names (e.g., "Spicy", "Fresh").
            food_types (list[str]): Types of food items for generating names (e.g., "Curry", "Salad").

        Warnings:
            If running in a production environment, a warning is logged to caution the user
            about potential risks of seeding data in production.

        Logs:
            Logs the initialization process and specifies the environment being used.

        """
        self.client = client
        self.config = get_config()
        self.environment = self.config.environment

        logger.info(f"Seeder - Initializing seeder for environment: {self.environment}")

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

        if self.environment == Environment.PRODUCTION:
            logger.warning("Seeder - Seeding data in production environment!")
        elif self.environment == Environment.DEVELOPMENT:
            self.categories.extend(["Test Category", "Debug Items"])

    def generate_fake_item(self) -> ItemCreate:
        """Generate a single fake menu item with environment-aware modifications."""
        try:
            adjective = fake.random_element(self.food_adjectives)
            food_type = fake.random_element(self.food_types)

            title = f"{adjective} {food_type}"
            if self.environment == Environment.PRODUCTION:
                title = f"[TEST] {title}"
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

            if self.environment != "production":
                item_data["description"] = f"[{self.environment}] {item_data['description']}"

            return ItemCreate(**item_data)

        except ValidationError as e:
            raise ValidationSeedingError(
                field_name=e.errors()[0]["loc"][0],
                invalid_value=e.errors()[0]["input"],
                validation_error=e,
            ) from e

        except Exception as e:
            raise ItemSeedingError(
                message="Seeder - Failed to generate item",
                original_error=e,
            ) from e

    async def seed_items(self, count: int = 10) -> None:
        """Seed items with environment-specific logging and safeguards."""
        logger.info(f"Seeder - Seeding {count} item(s) ...")

        # Safeguards for production
        if self.environment == Environment.PRODUCTION and count > 1:
            logger.warning("Seeder - Limiting seed count to 1 in production environment")
            count = 1

        seeded_count = 0
        errors = []

        for i in range(count):
            try:
                fake_item = self.generate_fake_item()
                item_dict = fake_item.model_dump()
                item_json_encoded = jsonable_encoder(item_dict)

                response = await self.client.table("item").insert(item_json_encoded).execute()

                logger.info(
                    "Seeder - Created item: title=%s; id=%s;",
                    response.data[0]["title"],
                    response.data[0]["id"],
                )
                seeded_count += 1

            except ItemSeedingError as e:
                logger.error(f"Seeder - Failed to seed item {i+1}/{count} in {self.environment}: {e!s}")
                errors.append(e)
            except (ValidationError, JSONDecodeError) as e:
                error = ItemSeedingError(
                    message=f"Seeder - Data validation error for item {i+1}/{count}",
                    original_error=e,
                )
                logger.error(str(error))
                errors.append(error)
            except (ValueError, TypeError) as e:
                error = ItemSeedingError(
                    message=f"Seeder - Data type error while seeding item {i+1}/{count}",
                    original_error=e,
                )
                logger.error(str(error))
                errors.append(error)

        if errors:
            raise ItemSeedingError(
                message=f"Seeder - Seeding completed with errors in {self.environment}. Seeded {seeded_count} of {count} items.",
                details={"errors": [{"error_id": e.error_id, "details": e.details} for e in errors]},
            )

        logger.info(f"Seeder - Successfully seeded {seeded_count} item(s) in environment: {self.environment}")

async def main(items: int = 1) -> None:
    """Run the seeding function with environment awareness."""
    config = get_config()
    client = await create_supabase()
    seeder = DataSeeder(client)

    try:
        await seeder.seed_items(items)
    except ItemSeedingError as e:
        logger.error(f"Seeder - Failed in {config.environment}: {e!s}")
        logger.error(f"Seeder - Error details: {e.details}")
    finally:
        await client.auth.sign_out()
