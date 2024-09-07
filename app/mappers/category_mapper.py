# app/mappers/category_mapper.py

from typing import Dict, Any, List
from app.mappers.base_mapper import BaseMapper
from app.models.domain.category import Category
from app.models.database.category import CategoryTable
from app.schemas.category import CategoryCreateDto, CategoryResponseDto


class CategoryMapper(BaseMapper[Category]):
    """
    Mapper class for the Category entity. Handles conversions between
    domain model, database model, and DTOs.
    """

    @classmethod
    def to_domain(cls, data: Dict[str, Any]) -> Category:
        """
        Convert a dictionary to a Category domain model instance.

        Args:
            data (Dict[str, Any]): The dictionary containing category data.

        Returns:
            Category: An instance of the Category domain model.
        """
        return Category(
            id=data.get('id'),
            name=data['name'],
            products=data.get('products', []),
            point_earning_rules=data.get('point_earning_rules', [])
        )

    @classmethod
    def to_dto(cls, domain_model: Category) -> CategoryResponseDto:
        """
        Convert a Category domain model instance to a CategoryResponseDto.

        Args:
            domain_model (Category): The Category domain model instance.

        Returns:
            CategoryResponseDto: A DTO representing the category.
        """
        return CategoryResponseDto(
            id=domain_model.id,
            name=domain_model.name
        )

    @classmethod
    def from_create_dto(cls, dto: CategoryCreateDto) -> Category:
        """
        Create a Category domain model instance from a CategoryCreateDto.

        Args:
            dto (CategoryCreateDto): The DTO containing data
            for creating a category.

        Returns:
            Category: A new instance of the Category domain model.
        """
        return Category(
            id=None,  # ID will be assigned by the database
            name=dto.name,
            products=[],
            point_earning_rules=[]
        )

    @classmethod
    def from_persistence(cls, db_model: CategoryTable) -> Category:
        """
        Convert a CategoryTable database model to a Category domain model.

        Args:
            db_model (CategoryTable): The database model instance.

        Returns:
            Category: An instance of the Category domain model.
        """
        return Category(
            id=db_model.id,
            name=db_model.name,
            products=[],  # These would typically be loaded separately or lazily # noqa: E501
            point_earning_rules=[]  # Same as products
        )

    @classmethod
    def to_persistence_model(cls, domain_model: Category) -> CategoryTable:
        """
        Convert a Category domain model to a CategoryTable database model.

        Args:
            domain_model (Category): The Category domain model instance.

        Returns:
            CategoryTable: An instance of the CategoryTable database model.
        """
        return CategoryTable(
            id=domain_model.id,
            name=domain_model.name
        )

    @classmethod
    def map_domain_list(cls, categories: List[Category]) -> List[CategoryResponseDto]:  # noqa: E501
        """
        Map a list of Category domain models to a list of CategoryResponseDto.

        Args:
            categories (List[Category]): A list of Category domain models.

        Returns:
            List[CategoryResponseDto]: A list of CategoryResponseDto instances.
        """
        return [cls.to_dto(category) for category in categories]
