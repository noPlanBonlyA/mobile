from fastapi import APIRouter, Depends, Query
from datetime import datetime
from .schemas import AllScheduleReadSchema
from .use_cases.get_schedule import GetScheduleUseCaseProtocol
from .use_cases.get_filtered_schedule import GetFilteredScheduleUseCaseProtocol
from .depends import get_schedule_use_case, get_filtered_schedule_use_case
from school_site.apps.users.depends import access_token_schema

router = APIRouter(prefix='/api/schedule', tags=['Schedule'])

@router.get('/', response_model=AllScheduleReadSchema, status_code=200)
async def get_schedule(
    access_token: str = Depends(access_token_schema),
    get_schedule_use_case: GetScheduleUseCaseProtocol = Depends(get_schedule_use_case)
):
    return await get_schedule_use_case(access_token)

@router.get('/lessons', response_model=AllScheduleReadSchema, status_code=200)
async def get_filtered_schedule(
    access_token: str = Depends(access_token_schema),
    datetime_start: datetime = Query(..., description="Start date for filtering"),
    datetime_end: datetime = Query(..., description="End date for filtering"),
    get_filtered_schedule_use_case: GetFilteredScheduleUseCaseProtocol = Depends(get_filtered_schedule_use_case)
):
    return await get_filtered_schedule_use_case(
        access_token=access_token,
        date_start=datetime_start,
        date_end=datetime_end
    )
