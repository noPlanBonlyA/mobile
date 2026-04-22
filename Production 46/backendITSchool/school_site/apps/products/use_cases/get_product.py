from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.products import ProductServiceProtocol 
from ..schemas import ProductReadSchema 

class GetProductUseCaseProtocol(UseCaseProtocol[ProductReadSchema]):
    async def __call__(self, product_id: UUID) -> ProductReadSchema:
        ...


class GetProductUseCase(GetProductUseCaseProtocol):
    def __init__(self, product_service: ProductServiceProtocol):
        self.product_service = product_service
    
    async def __call__(self, product_id: UUID) -> ProductReadSchema:
        return await self.product_service.get(product_id)
