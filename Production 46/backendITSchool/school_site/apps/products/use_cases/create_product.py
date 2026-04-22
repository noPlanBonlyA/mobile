from fastapi import UploadFile
from typing import Optional
import json
from school_site.core.use_cases import UseCaseProtocol 
from ..services.products import ProductServiceProtocol 
from school_site.apps.users.services.tokens import TokenServiceProtocol 
from ..schemas import ProductReadSchema, ProductCreateSchema

class CreateProductUseCaseProtocol(UseCaseProtocol[ProductReadSchema]):
    async def __call__(self, token: str, product_data: str, image: Optional[UploadFile]) -> ProductReadSchema:
        ...


class CreateProductUseCase(CreateProductUseCaseProtocol):
    def __init__(self, auth_service: TokenServiceProtocol, product_service: ProductServiceProtocol):
        self.auth_service = auth_service
        self.product_service = product_service
    
    async def __call__(self, token: str, product_data: str, image: Optional[UploadFile]) -> ProductReadSchema:
        await self.auth_service.get_admin_user(token)
        product = ProductCreateSchema(**json.loads(product_data))
        return await self.product_service.create(product, image)
