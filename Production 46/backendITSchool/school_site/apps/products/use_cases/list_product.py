from school_site.core.use_cases import UseCaseProtocol 
from ..services.products import ProductServiceProtocol 
from ..schemas import ProductPaginationResultSchema
from school_site.core.schemas import PaginationSchema


class GetListProductUseCaseProtocol(UseCaseProtocol[ProductPaginationResultSchema]):
    async def __call__(self,
                       limit: int = 10,
                       offset: int = 0) -> ProductPaginationResultSchema:
        ...


class GetListProductUseCase(GetListProductUseCaseProtocol):
    def __init__(self, product_service: ProductServiceProtocol):
        self.product_service = product_service
    
    async def __call__(self, 
                       limit: int = 10,
                       offset: int = 0) -> ProductPaginationResultSchema:
        pagination = PaginationSchema(
            limit=limit,
            offset=offset
        )
        return await self.product_service.list(pagination)
