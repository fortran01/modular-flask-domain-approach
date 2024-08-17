# app/schemas/category.py
from pydantic import BaseModel


class CategoryCreateDto(BaseModel):
    """
    Data Transfer Object for creating a new category.

    Attributes:
        name (str): The name of the category.
    """
    name: str


class CategoryResponseDto(BaseModel):
    """
    Data Transfer Object for responding with category information.

    Attributes:
        id (int): The unique identifier of the category.
        name (str): The name of the category.
    """
    id: int
    name: str
