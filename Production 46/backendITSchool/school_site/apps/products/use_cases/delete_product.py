from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.products import ProductServiceProtocol 
from school_site.apps.users.services.tokens import TokenServiceProtocol 


class DeleteProductUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, token: str, product_id: UUID) -> None:
        ...


class DeleteProductUseCase(DeleteProductUseCaseProtocol):
    def __init__(self, auth_service: TokenServiceProtocol, product_service: ProductServiceProtocol):
        self.auth_service = auth_service
        self.product_service = product_service
    
    async def __call__(self, token: str, product_id: UUID) -> None:
        await self.auth_service.get_admin_user(token)
        return await self.product_service.delete(product_id)
