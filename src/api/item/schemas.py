# ruff: noqa: D101, D102, D106
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ItemBase(BaseModel):
    title: str = Field(max_length=22, examples=["Mystery Curry"])
    price: Decimal = Field(decimal_places=2, ge=0, examples=["12.50"], description="Amount with 2 decimal places")
    is_available: bool

    @field_validator("title")
    @classmethod
    def convert_empty_to_none(cls, v: str | None) -> str | None:
        """Convert empty strings to None."""
        return v or None

    @field_validator("price")
    @classmethod
    def validate_decimal_places(cls, v: Decimal | None) -> Decimal | None:
        """Ensure the price has exactly two decimal places."""
        if v is None:
            return None
        return v.quantize(Decimal("0.01"))


class ItemCreate(ItemBase):
    """Model for creating a new item."""

    title_full: str | None = Field(None, examples=["Yellow Curry with seasonal seafood"])
    description: str | None = Field(
        None,
        examples=["Southern-style Yellow Curry cooked with seasonal seafood."],
    )
    categories: list[UUID] | None = None
    image_uri: str | None = Field(None, examples=["https://www.example.com/yellow_curry.png"])
    created_at: datetime | None = None


class ItemUpdate(ItemBase):
    """Model for updating an existing item. All fields are optional."""

    title: str | None = Field(None, max_length=22, examples=["Red Curry"])
    title_full: str | None = Field(None, examples=["Red Curry with river herbs"])
    description: str | None = Field(
        None,
        examples=["Central-style Red Curry cooked with delicious herbs river herbs."],
    )
    categories: list[UUID] | None = None
    price: Decimal | None = Field(None, decimal_places=2, ge=0, examples=["15.00"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/red_curry.png"])
    updated_at: datetime | None = None
    is_available: bool | None = None


class Item(ItemBase):
    """Model representing the complete item."""

    id: UUID | None = None
    title_full: str | None = Field(None, examples=["Green Curry"])
    description: str | None = Field(
        None,
        examples=["Northern-style Green Curry cooked in clay pots."],
    )
    categories: list[UUID] | None = None
    image_uri: str | None = Field(None, examples=["https://www.example.com/green_curry.png"])
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class ConfigDict:
        json_encoders: ClassVar[dict] = {Decimal: str}
        json_schema_extra: ClassVar[dict] = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Mystery Curry",
                "title_full": "Mysterious Curry with an assortment of pickled vegetables",
                "description": "Mystery Curry from another planet!",
                "categories": ["123e4567-e89b-12d3-a456-426614174001"],
                "price": "12.50",
                "image_uri": "https://www.example.com/mystery_curry.png",
                "created_at": "2023-10-24T12:00:00Z",
                "updated_at": "2023-10-25T12:00:00Z",
                "is_available": True,
            },
        }


class ItemResponseModel(BaseModel):
    """Response model for returning a list of items with a count."""

    data: list[Item]
    count: int | None = Field(None, examples=[1])
