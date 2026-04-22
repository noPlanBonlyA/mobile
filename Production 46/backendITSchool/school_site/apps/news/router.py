from fastapi import APIRouter, Response, Depends, \
    Form, UploadFile, File, Query
from uuid import UUID
from typing import Optional
from .schemas import (
    NewsReadSchema,
    PaginationResultSchema,
    NewsWithPhotoPaginationResultSchema,
    NewsWithPhotoReadSchema
)
from .depends import (
    get_get_all_news_use_case,
    get_create_news_use_case,
    get_delete_news_use_case,
    get_get_news_use_case,
    get_update_news_use_case
)
from .use_cases.create_news import CreateNewsUseCaseProtocol
from .use_cases.delete_news import DeleteNewsUseCaseProtocol
from .use_cases.get_all_news import GetAllNewsUseCaseProtocol
from .use_cases.get_news_by_id import GetNewsUseCaseProtocol
from .use_cases.update_news import UpdateNewsUseCaseProtocol

router = APIRouter(prefix='/api/news', tags=['News'])

@router.post('/', response_model=NewsWithPhotoReadSchema, status_code=201)
async def create_news(
    news_data: str = Form(...),
    image: Optional[UploadFile] = File(None),
    create_news_use_case: CreateNewsUseCaseProtocol = Depends(get_create_news_use_case)
) -> NewsWithPhotoReadSchema:
    return await create_news_use_case(news_data, image)

@router.get('/', response_model=NewsWithPhotoPaginationResultSchema)
async def get_all_news(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    get_all: GetAllNewsUseCaseProtocol = Depends(get_get_all_news_use_case)
) -> PaginationResultSchema[NewsReadSchema]:
    return await get_all(limit, offset)

@router.get('/{news_id}', response_model=NewsWithPhotoReadSchema)
async def get_news_by_id(
    news_id: UUID,
    get_news_use_case: GetNewsUseCaseProtocol = Depends(get_get_news_use_case)
) -> NewsWithPhotoReadSchema:
    return await get_news_use_case(news_id)

@router.put('/{news_id}', response_model=NewsWithPhotoReadSchema)
async def update_news(
    news_id: UUID,
    news_data: str = Form(...),
    image: Optional[UploadFile] = File(None),
    update_news_use_case: UpdateNewsUseCaseProtocol = Depends(get_update_news_use_case)
) -> NewsWithPhotoReadSchema:
    return await update_news_use_case(news_id, news_data, image)
    
@router.delete('/{news_id}', status_code=204)
async def delete_news(
    news_id: UUID,
    delete_news_use_case: DeleteNewsUseCaseProtocol = Depends(get_delete_news_use_case)
) -> Response:
    await delete_news_use_case(news_id)
    return None