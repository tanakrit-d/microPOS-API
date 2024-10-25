# ruff: noqa: D101, D102, D106
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class Item(BaseModel):
    id: UUID | None = None
    title: str | None = Field(max_length=22, examples=["Fried Rice"])
    title_full: str | None = Field(None, examples=["Thai-style Fried Rice with Pineapple"])
    description: str | None = Field(
        None,
        examples=["Thai-style Fried Rice, consisting of a fiery and sweet blend of Chilli and Pineapple"],
    )
    categories: list[UUID] | None = None
    price: Decimal = Field (decimal_places=2, ge=0, examples=["18.50"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/fried_rice.png"])
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_available: bool

    @field_validator("title", "title_full", "description", mode="before")
    def convert_empty_to_none(self, v: str | None) -> str | None:
        return v or None

    @field_validator("price", mode="before")
    def validate_decimal_places(self, v: Decimal | None) -> Decimal | None:
        if v is None:
            return None
        return v.quantize(Decimal("0.01"))

    class Config:
        json_encoders: ClassVar[dict] = {Decimal: str}
        schema_extra: ClassVar[dict] = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Fried Rice",
                "title_full": "Thai-style Fried Rice with Pineapple",
                "description": "Thai-style Fried Rice, consisting of a fiery and sweet blend of Chilli and Pineapple",
                "categories": ["123e4567-e89b-12d3-a456-426614174001"],
                "price": "18.50",
                "image_uri": "https://www.example.com/fried_rice.png",
                "created_at": "2023-10-24T12:00:00Z",
                "updated_at": "2023-10-24T12:00:00Z",
                "is_available": True,
            },
        }


class ItemCreate(BaseModel):
    title: str = Field(max_length=22, examples=["Tomato Soup"])
    title_full: str | None = Field(None, examples=["Heirloom Tomato Soup"])
    description: str | None = Field(
        None,
        examples=["Tomato Soup made with pureed Heirloom Tomatoes and Roasted Peppercorns"],
    )
    categories: list[UUID] | None = None
    price: Decimal = Field(decimal_places=2, ge=0, examples=["12.50"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/tomato_soup.png"])
    created_at: datetime | None = None
    is_available: bool = False


class ItemUpdate(BaseModel):
    title: str | None = Field(None, max_length=22, examples=["French Fries"])
    title_full: str | None = Field(None, examples=["Hand-cut French Fries"])
    description: str | None = Field(
        None,
        examples=[
            "Russet Potatoes, hand-cut by a Buddhist Monk into the ancient pre-cursor to French Fries - and then fried (French style)",
        ],
    )
    categories: list[UUID] | None = None
    price: Decimal | None = Field(None, decimal_places=2, examples=["15.00"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/french_fries.png"])
    updated_at: datetime | None = None
    is_available: bool | None = None


class ItemResponseModel(BaseModel):
    data: list[Item]
    count: int | None = Field(None, examples=[1])
