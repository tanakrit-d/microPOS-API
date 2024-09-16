# ruff: noqa: D103
from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from supabase import AClient, PostgrestAPIResponse

from src.api.category.schemas import CategoryCreate, CategoryResponseModel, CategoryUpdate
from src.database import get_supabase_client
from utils.exceptions import get_error_id
from utils.logging import logger

router = APIRouter(
    prefix="/category",
    tags=["Category"],
)


@router.get(
    "/{cat_id}",
    summary="Get Category",
    description="Retrieve a category by id.",
    response_model=CategoryResponseModel,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    cat_id: UUID,
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[CategoryResponseModel]:
    try:
        response = await client.table("category").select("*", count="exact").eq("id", cat_id).execute()
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to retrieve category: %s", error_id, cat_id)
        raise HTTPException(
            status_code=500,
            detail=f"Error ID: {error_id}; Failed to retrieve category",
        ) from e
    else:
        return response


@router.get(
    "/",
    summary="Get All Categories",
    description="Retrieve all categories.",
    response_model=CategoryResponseModel,
    status_code=status.HTTP_200_OK,
)
async def get_categories(
    client: Annotated[AClient, Depends(get_supabase_client)],
    available: bool | None = Query(None, description="Filter by availability"),
) -> PostgrestAPIResponse[CategoryResponseModel]:
    try:
        if available is None:
            response = await client.table("category").select("*", count="exact").execute()
        else:
            response = await client.table("category").select("*", count="exact").eq("is_available", f"{available}").execute()
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to retrieve categories", error_id)
        raise HTTPException(
            status_code=500,
            detail="Error ID: {error_id}; Failed to retrieve categories",
        ) from e
    else:
        return response


@router.post(
    "/create",
    summary="Create Category",
    description="Create a new category.",
    response_model=CategoryResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category: CategoryCreate,
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[CategoryResponseModel]:
    try:
        category_dict = category.model_dump()
        category_dict["created_at"] = datetime.now(timezone.utc)
        category_json_encoded = jsonable_encoder(category_dict)
        response = await client.table("category").insert(category_json_encoded).execute()
        logger.info(
            "Created category: title=%s; id=%s",
            response.data[0]["title"],
            response.data[0]["id"],
        )
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to create category", error_id)
        raise HTTPException(
            status_code=500,
            detail=f"Error ID: {error_id}; Failed to create category: {category_dict["title"]}",
        ) from e
    else:
        return response


@router.patch(
    "/{cat_id}",
    summary="Update Category",
    description="Update a category.",
    response_model=CategoryResponseModel,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    cat_id: UUID,
    category: CategoryUpdate,
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[CategoryResponseModel]:
    try:
        category_dict = category.model_dump(exclude_unset=True)
        category_dict["updated_at"] = datetime.now(timezone.utc)
        category_json_encoded = jsonable_encoder(category_dict)
        response = await client.table("category").update(category_json_encoded).eq("id", cat_id).execute()
        logger.info(
            "Updated category: title=%s; id=%s",
            response.data[0]["title"],
            response.data[0]["id"],
        )
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to update category: %s", error_id, cat_id)
        raise HTTPException(
            status_code=500,
            detail=f"Error ID: {error_id}; Failed to update category",
        ) from e
    else:
        return response


@router.delete(
    "/{cat_id}",
    summary="Delete Category",
    description="Delete a category by id.",
    response_model=CategoryResponseModel,
    status_code=status.HTTP_200_OK,
)
async def delete_category(
    cat_id: UUID,
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[CategoryResponseModel]:
    try:
        response = await client.table("category").delete().eq("id", cat_id).execute()
        logger.info(
            "Deleted category: title=%s; id=%s",
            response.data[0]["title"],
            response.data[0]["id"],
        )
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to delete category: %s", error_id, cat_id)
        raise HTTPException(
            status_code=500,
            detail=f"Error ID: {error_id}; Failed to delete category",
        ) from e
    else:
        return response
