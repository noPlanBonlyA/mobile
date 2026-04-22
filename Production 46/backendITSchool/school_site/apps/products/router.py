from fastapi import APIRouter, Depends, Path, UploadFile, File, Form, Query
from uuid import UUID
from typing import Optional
from .use_cases.create_product import CreateProductUseCaseProtocol
from .use_cases.update_product import UpdateProductUseCaseProtocol
from .use_cases.get_product import GetProductUseCaseProtocol
from .use_cases.delete_product import DeleteProductUseCaseProtocol
from .use_cases.list_product import GetListProductUseCaseProtocol
from .use_cases.create_photo import CreatePhotoUseCaseProtocol
from .use_cases.update_photo import UpdatePhotoUseCaseProtocol
from .use_cases.delete_photo import DeletePhotoUseCaseProtocol
from .use_cases.get_photo import GetPhotoUseCaseProtocol
from .use_cases.list_available_products import GetAvailableListProductUseCaseProtocol
from .use_cases.list_not_available_products import GetNotAvailableListProductUseCaseProtocol
from .depends import (
    get_product_create_use_case, get_product_update_use_case, get_product_get_use_case,
    get_product_delete_use_case, get_product_get_list_use_case, get_photo_create_use_case,
    get_photo_update_use_case, get_photo_delete_use_case, get_photo_get_use_case,
    get_available_products_use_case, get_not_available_products_use_case,
) 
from .schemas import ProductReadSchema, ProductPaginationResultSchema, PhotoReadSchema
from school_site.apps.users.depends import access_token_schema

router = APIRouter(prefix='/api/products', tags=['Products'])


@router.get("/available", response_model=ProductPaginationResultSchema)
async def list_available_products(
    access_token: str = Depends(access_token_schema),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    price: int = Query(..., ge=0),
    list_available: GetAvailableListProductUseCaseProtocol = Depends(get_available_products_use_case)
):
    products = await list_available(price, limit, offset)
    return products


@router.get("/not-available", response_model=ProductPaginationResultSchema)
async def list_not_available_products(
    access_token: str = Depends(access_token_schema),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    price: int = Query(..., ge=0),
    not_list_available: GetNotAvailableListProductUseCaseProtocol = Depends(get_not_available_products_use_case)
):
    products = await not_list_available(price, limit, offset)
    return products


@router.post("/", response_model=ProductReadSchema)
async def create_product(
    product_data: str = Form(...),
    access_token: str = Depends(access_token_schema),
    image: Optional[UploadFile] = File(None),
    create: CreateProductUseCaseProtocol = Depends(get_product_create_use_case)
):
    created_product = await create(access_token, product_data, image)
    return created_product


@router.put("/{product_id}", response_model=ProductReadSchema)
async def update_product(
    product_data: str = Form(...),
    product_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    image: Optional[UploadFile] = File(None),
    update: UpdateProductUseCaseProtocol = Depends(get_product_update_use_case)
):
    updated_product = await update(access_token, product_id, product_data, image)
    return updated_product


@router.get("/{product_id}", response_model=ProductReadSchema)
async def get_product(
    access_token: str = Depends(access_token_schema),
    product_id: UUID = Path(...),
    get: GetProductUseCaseProtocol = Depends(get_product_get_use_case)
):
    product = await get(product_id)
    return product


@router.get("/", response_model=ProductPaginationResultSchema)
async def list_products(
    access_token: str = Depends(access_token_schema),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    list: GetListProductUseCaseProtocol = Depends(get_product_get_list_use_case)
):
    products = await list(limit, offset)
    return products
    

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    delete: DeleteProductUseCaseProtocol = Depends(get_product_delete_use_case)
):
    await delete(access_token, product_id)

    return None


@router.post("/{product_id}/photo/", response_model=PhotoReadSchema)
async def create_photo(
    photo_data: str = Form(...),
    product_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    image: Optional[UploadFile] = File(...),
    create_photo: CreatePhotoUseCaseProtocol = Depends(get_photo_create_use_case)
):
    return await create_photo(access_token, product_id, photo_data, image)


@router.put("/{product_id}/photo/{photo_id}", response_model=PhotoReadSchema)
async def update_photo(
    photo_data: str = Form(...),
    product_id: UUID = Path(...),
    photo_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    image: Optional[UploadFile] = File(...),
    update_photo: UpdatePhotoUseCaseProtocol = Depends(get_photo_update_use_case)
):
    return await update_photo(access_token, product_id, photo_id, photo_data, image)


@router.delete("/{product_id}/photo/{photo_id}", status_code=204)
async def delete_photo(
    product_id: UUID = Path(...),
    photo_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    delete_photo: DeletePhotoUseCaseProtocol = Depends(get_photo_delete_use_case)
):
    await delete_photo(access_token, photo_id)

    return None


@router.get("/{product_id}/photo/{photo_id}", response_model=PhotoReadSchema)
async def get_photo(
    access_token: str = Depends(access_token_schema),
    product_id: UUID = Path(...),
    photo_id: UUID = Path(...),
    get_photo: GetPhotoUseCaseProtocol = Depends(get_photo_get_use_case)
):
    return await get_photo(photo_id)