# ruff: noqa: D101, D102, D106
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ItemBase(BaseModel):
    title: str = Field(max_length=22, examples=["Sample Item"])
    price: Decimal = Field(decimal_places=2, ge=0, examples=["12.50"], description="Amount with 2 decimal places")
    is_available: bool

    @field_validator("title", "description", mode="before")
    def convert_empty_to_none(self, v: str | None) -> str | None:
        """Convert empty strings to None."""
        return v or None

    @field_validator("price", mode="before")
    def validate_decimal_places(self, v: Decimal | None) -> Decimal | None:
        """Ensure the price has exactly two decimal places."""
        if v is None:
            return None
        return v.quantize(Decimal("0.01"))


class ItemCreate(ItemBase):
    """Model for creating a new item."""

    title_full: str | None = Field(None, examples=["Detailed Sample Item"])
    description: str | None = Field(
        None,
        examples=["A detailed description of the item, describing its features and qualities."],
    )
    categories: list[UUID] | None = None
    image_uri: str | None = Field(None, examples=["https://www.example.com/sample_item.png"])
    created_at: datetime | None = None


class ItemUpdate(ItemBase):
    """Model for updating an existing item. All fields are optional."""

    title: str | None = Field(None, max_length=22, examples=["Updated Item"])
    title_full: str | None = Field(None, examples=["Updated Detailed Sample Item"])
    description: str | None = Field(
        None,
        examples=["An updated description for the item."],
    )
    categories: list[UUID] | None = None
    price: Decimal | None = Field(None, decimal_places=2, ge=0, examples=["15.00"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/updated_item.png"])
    updated_at: datetime | None = None
    is_available: bool | None = None


class Item(ItemBase):
    """Model representing the complete item."""

    id: UUID | None = None
    title_full: str | None = Field(None, examples=["Detailed Sample Item"])
    description: str | None = Field(
        None,
        examples=["A detailed description of the item, describing its features and qualities."],
    )
    categories: list[UUID] | None = None
    image_uri: str | None = Field(None, examples=["https://www.example.com/sample_item.png"])
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        json_encoders: ClassVar[dict] = {Decimal: str}
        schema_extra: ClassVar[dict] = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Sample Item",
                "title_full": "Detailed Sample Item",
                "description": "A detailed description of the item, describing its features and qualities.",
                "categories": ["123e4567-e89b-12d3-a456-426614174001"],
                "price": "12.50",
                "image_uri": "https://www.example.com/sample_item.png",
                "created_at": "2023-10-24T12:00:00Z",
                "updated_at": "2023-10-25T12:00:00Z",
                "is_available": True,
            },
        }


class ItemResponseModel(BaseModel):
    """Response model for returning a list of items with a count."""

    data: list[Item]
    count: int | None = Field(None, examples=[1])
