# app/mappers/shopping_cart_mapper.py

from typing import Dict, Any, List
from app.mappers.base_mapper import BaseMapper
from app.models.domain.shopping_cart import ShoppingCart, ShoppingCartItem
from app.models.database.shopping_cart import (
    ShoppingCartTable,
    ShoppingCartItemTable,
)
from app.schemas.shopping_cart import (
    ShoppingCartResponseDto,
    ShoppingCartItemDto,
)
from app.mappers.product_mapper import ProductMapper


class ShoppingCartMapper(BaseMapper[ShoppingCart]):
    """
    Mapper class for the ShoppingCart entity. Handles conversions between
    domain model, database model, and DTOs.
    """

    @classmethod
    def to_domain(cls, data: Dict[str, Any]) -> ShoppingCart:
        """
        Convert a dictionary to a ShoppingCart domain model instance.

        Args:
            data (Dict[str, Any]): The dictionary containing shopping
                cart data.

        Returns:
            ShoppingCart: An instance of the ShoppingCart domain model.
        """
        return ShoppingCart(
            id=data.get('id'),
            customer_id=data['customer_id'],
            items=[cls._item_to_domain(item) for item in data.get('items', [])]
        )

    @classmethod
    def to_dto(cls, domain_model: ShoppingCart) -> ShoppingCartResponseDto:
        """
        Convert a ShoppingCart domain model instance to a
        ShoppingCartResponseDto.

        Args:
            domain_model (ShoppingCart): The ShoppingCart domain
            model instance.

        Returns:
            ShoppingCartResponseDto: A DTO representing the shopping cart.
        """
        return ShoppingCartResponseDto(
            id=domain_model.id,
            customer_id=domain_model.customer_id,
            items=[cls._item_to_dto(item) for item in domain_model.items]
        )

    @classmethod
    def to_persistence(cls, domain_model: ShoppingCart) -> Dict[str, Any]:
        """
        Convert a ShoppingCart domain model instance to a dictionary
        suitable for database persistence.

        Args:
            domain_model (ShoppingCart): The ShoppingCart domain
            model instance.

        Returns:
            Dict[str, Any]: A dictionary representing the shopping cart
              for persistence.
        """
        return {
            'id': domain_model.id,
            'customer_id': domain_model.customer_id,
            'items': [cls._item_to_persistence(item) for item in
                      domain_model.items]
        }

    @classmethod
    def from_persistence(cls, db_model: ShoppingCartTable) -> ShoppingCart:
        """
        Convert a ShoppingCartTable database model to a ShoppingCart
        domain model.

        Args:
            db_model (ShoppingCartTable): The database model instance.

        Returns:
            ShoppingCart: An instance of the ShoppingCart domain model.
        """
        return ShoppingCart(
            id=db_model.id,
            customer_id=db_model.customer_id,
            items=[cls._item_from_persistence(item) for item in db_model.items]
        )

    @classmethod
    def to_persistence_model(
        cls, domain_model: ShoppingCart
    ) -> ShoppingCartTable:
        """
        Convert a ShoppingCart domain model to a ShoppingCartTable
        database model.

        Args:
            domain_model (ShoppingCart): The ShoppingCart domain
            model instance.

        Returns:
            ShoppingCartTable: An instance of the ShoppingCartTable
                database model.
        """
        return ShoppingCartTable(
            id=domain_model.id,
            customer_id=domain_model.customer_id,
            items=[cls._item_to_persistence_model(
                item) for item in domain_model.items]
        )

    @classmethod
    def map_domain_list(
        cls, carts: List[ShoppingCart]
    ) -> List[ShoppingCartResponseDto]:
        """
        Map a list of ShoppingCart domain models to a list of
        ShoppingCartResponseDto.

        Args:
            carts (List[ShoppingCart]): A list of ShoppingCart domain models.

        Returns:
            List[ShoppingCartResponseDto]: A list of ShoppingCartResponseDto
                instances.
        """
        return [cls.to_dto(cart) for cart in carts]

    @classmethod
    def _item_to_domain(cls, data: Dict[str, Any]) -> ShoppingCartItem:
        """Convert a dictionary to a ShoppingCartItem domain model instance."""
        return ShoppingCartItem(
            product=ProductMapper.to_domain(data['product']),
            quantity=data['quantity']
        )

    @classmethod
    def _item_to_dto(cls, item: ShoppingCartItem) -> ShoppingCartItemDto:
        """Convert a ShoppingCartItem domain model to a ShoppingCartItemDto."""
        return ShoppingCartItemDto(
            product=ProductMapper.to_dto(item.product),
            quantity=item.quantity
        )

    @classmethod
    def _item_to_persistence(cls, item: ShoppingCartItem) -> Dict[str, Any]:
        """Convert ShoppingCartItem domain model to dict for persistence."""
        return {
            'product_id': item.product.id,
            'quantity': item.quantity
        }

    @classmethod
    def _item_from_persistence(
        cls, db_item: ShoppingCartItemTable
    ) -> ShoppingCartItem:
        """Convert ShoppingCartItemTable to ShoppingCartItem."""
        return ShoppingCartItem(
            product=ProductMapper.from_persistence(db_item.product),
            quantity=db_item.quantity
        )

    @classmethod
    def _item_to_persistence_model(
        cls, item: ShoppingCartItem
    ) -> ShoppingCartItemTable:
        """Convert ShoppingCartItem to ShoppingCartItemTable."""
        return ShoppingCartItemTable(
            product_id=item.product.id,
            quantity=item.quantity
        )
