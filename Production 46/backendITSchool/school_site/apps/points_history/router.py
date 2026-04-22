from fastapi import APIRouter, Depends, Query
from school_site.apps.users.depends import access_token_schema
from .depends import (
    get_create_points_history_use_case,
    get_get_points_history_by_user_use_case
)
from .use_cases.create_points_history_use_case import CreatePointsHistoryUseCaseProtocol
from .use_cases.get_points_hystory_by_user_use_case import GetPointsHistoryByUserUseCaseProtocol
from .schemas import (
    PointsHistoryCreateSchema,
    PointsHistoryReadSchema,
    PointsHistoryPaginationSchema
)

router = APIRouter(prefix='/api/points/history', tags=['PointsHistory'])

@router.post('/', response_model=PointsHistoryReadSchema, status_code=201)
async def create_points_history(
    history: PointsHistoryCreateSchema,
    access_token: str = Depends(access_token_schema),
    use_case: CreatePointsHistoryUseCaseProtocol = Depends(get_create_points_history_use_case)
) -> PointsHistoryReadSchema:
    return await use_case(history, access_token)

@router.get('/student', response_model=PointsHistoryPaginationSchema)
async def get_points_history_by_user(
    limit: int = Query(10, ge=1, le=100, description="Number of points history to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),

    access_token: str = Depends(access_token_schema),
    use_case: GetPointsHistoryByUserUseCaseProtocol = Depends(get_get_points_history_by_user_use_case)
) -> PointsHistoryPaginationSchema:
    return await use_case(access_token, limit, offset)