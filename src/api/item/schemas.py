# ruff: noqa: D101
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: UUID | None = None
    title: str | None = Field(None, max_length=22, examples=["Fried Rice"])
    title_full: str | None = Field(None, examples=["Thai-style Fried Rice with Pineapple"])
    description: str | None = Field(
        None,
        examples=["Thai-style Fried Rice, consisting of a fiery and sweet blend of Chilli and Pineapple"],
    )
    categories: list[UUID] | None = None
    price: float | None = Field(0.0, examples=["18.50"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/fried_rice.png"])
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_available: bool | None = None


class ItemCreate(BaseModel):
    title: str = Field(max_length=22, examples=["Tomato Soup"])
    title_full: str | None = Field(None, examples=["Heirloom Tomato Soup"])
    description: str | None = Field(
        None,
        examples=["Tomato Soup made with pureed Heirloom Tomatoes and Roasted Peppercorns"],
    )
    categories: list[UUID] | None = None
    price: float = Field(0.0, examples=["12.50"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/tomato_soup.png"])
    created_at: datetime = None
    is_available: bool = False


class ItemUpdate(Item):
    title: str = Field(max_length=22, examples=["French Fries"])
    title_full: str | None = Field(None, examples=["Hand-cut French Fries"])
    description: str | None = Field(
        None,
        examples=[
            "Russet Potatoes, hand-cut by a Buddhist Monk into the ancient pre-cursor to French Fries - and then fried (French style)",
        ],
    )
    categories: list[UUID] | None = None
    price: float = Field(0.0, examples=["15.00"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/french_fries.png"])
    updated_at: datetime = None
    is_available: bool = False


class ItemResponseModel(BaseModel):
    data: list[Item]
    count: int | None = Field(None, examples=[1])
