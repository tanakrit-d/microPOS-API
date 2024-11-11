# ruff: noqa: D101
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Category(BaseModel):
    id: UUID | None = None
    title: str | None = Field(None, max_length=22, examples=["Mains"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/steak_and_potatoes.png"])
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_available: bool | None = None


class CategoryCreate(BaseModel):
    title: str = Field(max_length=22, examples=["Sides"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/smoothies.png"])
    created_at: datetime = None
    is_available: bool = False


class CategoryUpdate(BaseModel):
    title: str | None = Field(None, max_length=22, examples=["Desserts"])
    image_uri: str | None = Field(None, examples=["https://www.example.com/lime_gelato.png"])
    updated_at: datetime = None
    is_available: bool | None = False


class CategoryResponseModel(BaseModel):
    data: list[Category]
    count: int | None = Field(None, examples=[1])
