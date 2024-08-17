# app/schemas/product.py
from pydantic import BaseModel
from typing import Optional


class ProductCreateDto(BaseModel):
    """
    Data Transfer Object for creating a new product.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        category_id (int): The identifier of the category this product
        belongs to.
        image_url (Optional[str]): The URL of the product's image,
            if available.
    """
    name: str
    price: float
    category_id: int
    image_url: Optional[str] = None


class ProductUpdateDto(BaseModel):
    """
    Data Transfer Object for updating an existing product.

    Attributes:
        name (Optional[str]): The updated name of the product, if provided.
        price (Optional[float]): The updated price of the product, if provided.
        category_id (Optional[int]): The updated identifier of the category
            this product belongs to, if provided.
        image_url (Optional[str]): The updated URL of the product's image,
            if provided.
    """
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None


class ProductResponseDto(BaseModel):
    """
    Data Transfer Object for responding with product information.

    Attributes:
        id (int): The unique identifier of the product.
        name (str): The name of the product.
        price (float): The price of the product.
        category_id (int): The identifier of the category this product
          belongs to.
        image_url (Optional[str]): The URL of the product's image,
        if available.
    """
    id: int
    name: str
    price: float
    category_id: int
    image_url: Optional[str] = None
