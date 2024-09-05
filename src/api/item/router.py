# ruff: noqa: D103
from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from supabase import AClient, PostgrestAPIResponse

from src.api.item.schemas import ItemCreate, ItemResponseModel, ItemUpdate
from src.database import get_supabase_client
from utils.exceptions import get_error_id
from utils.logging import logger

router = APIRouter(
    prefix="/item",
    tags=["Items"],
)


@router.get(
    "/{item_id}",
    summary="Get Menu Item",
    description="Retrieve a menu item by id.",
    response_model=ItemResponseModel,
    status_code=status.HTTP_200_OK,
)
async def get_item(
    item_id: UUID,
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[ItemResponseModel]:
    try:
        response = await client.table("item").select("*", count="exact").eq("id", item_id).execute()
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to retrieve item: %s", error_id, item_id)
        raise HTTPException(
            status_code=500,
            detail=f"Error ID: {error_id}; Failed to retrieve item",
        ) from e
    else:
        return response


@router.get(
    "/",
    summary="Get All Menu Items",
    description="Retrieve all menu items.",
    response_model=ItemResponseModel,
    status_code=status.HTTP_200_OK,
)
async def get_items(
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[ItemResponseModel]:
    try:
        response = await client.table("item").select("*", count="exact").execute()
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to retrieve items", error_id)
        raise HTTPException(
            status_code=500,
            detail="Error ID: {error_id}; Failed to retrieve items",
        ) from e
    else:
        return response


@router.post(
    "/create",
    summary="Create Menu Item",
    description="Create a new menu item.",
    response_model=ItemResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(
    item: ItemCreate,
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[ItemResponseModel]:
    try:
        item_dict = item.model_dump()
        item_dict["created_at"] = datetime.now(timezone.utc)
        item_json_encoded = jsonable_encoder(item_dict)
        response = await client.table("item").insert(item_json_encoded).execute()
        logger.info(
            "Created item: title=%s; id=%s",
            response.data[0]["title"],
            response.data[0]["id"],
        )
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to create item", error_id)
        raise HTTPException(
            status_code=500,
            detail=f"Error ID: {error_id}; Failed to create item: {item_dict["title"]}",
        ) from e
    else:
        return response


@router.patch(
    "/{item_id}",
    summary="Update Menu Item",
    description="Update a menu item.",
    response_model=ItemResponseModel,
    status_code=status.HTTP_200_OK,
)
async def update_item(
    item_id: UUID,
    item: ItemUpdate,
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[ItemResponseModel]:
    try:
        item_dict = item.model_dump(exclude_unset=True)
        item_dict["updated_at"] = datetime.now(timezone.utc)
        item_json_encoded = jsonable_encoder(item_dict)
        response = await client.table("item").update(item_json_encoded).eq("id", item_id).execute()
        logger.info(
            "Updated item: title=%s; id=%s",
            response.data[0]["title"],
            response.data[0]["id"],
        )
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to update item: %s", error_id, item_id)
        raise HTTPException(
            status_code=500,
            detail=f"Error ID: {error_id}; Failed to update item",
        ) from e
    else:
        return response


@router.delete(
    "/{item_id}",
    summary="Delete Menu Item",
    description="Delete a menu item by id.",
    response_model=ItemResponseModel,
    status_code=status.HTTP_200_OK,
)
async def delete_item(
    item_id: UUID,
    client: Annotated[AClient, Depends(get_supabase_client)],
) -> PostgrestAPIResponse[ItemResponseModel]:
    try:
        response = await client.table("item").delete().eq("id", item_id).execute()
        logger.info(
            "Deleted item: title=%s; id=%s",
            response.data[0]["title"],
            response.data[0]["id"],
        )
    except Exception as e:
        error_id = get_error_id()
        logger.exception("Error ID: %s; Failed to delete item: %s", error_id, item_id)
        raise HTTPException(
            status_code=500,
            detail=f"Error ID: {error_id}; Failed to delete item",
        ) from e
    else:
        return response
