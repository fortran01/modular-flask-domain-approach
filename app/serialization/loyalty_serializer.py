# app/serialization/loyalty_serializer.py
from app.serialization.base_serializer import BaseSerializer
from app.schemas.checkout import CheckoutResponseDto
from app.schemas.points import PointsDto
from app.schemas.shopping_cart import ShoppingCartResponseDto


class LoyaltySerializer(BaseSerializer):
    @staticmethod
    def serialize_checkout_response(
        checkout: CheckoutResponseDto
    ) -> dict:
        """
        Serializes a CheckoutResponseDto into a dictionary.

        Args:
            checkout (CheckoutResponseDto): The checkout response data.

        Returns:
            dict: The serialized checkout response.
        """
        return BaseSerializer.serialize(checkout)

    @staticmethod
    def serialize_points(points: PointsDto) -> dict:
        """
        Serializes a PointsDto into a dictionary.

        Args:
            points (PointsDto): The points data.

        Returns:
            dict: The serialized points data.
        """
        return BaseSerializer.serialize(points)

    @staticmethod
    def serialize_shopping_cart(cart_dto: ShoppingCartResponseDto) -> dict:
        """
        Serializes a ShoppingCartResponseDto into a dictionary.

        Args:
            cart_dto (ShoppingCartResponseDto): The shopping cart data
                transfer object.

        Returns:
            dict: The serialized shopping cart data.
        """
        return BaseSerializer.serialize(cart_dto)
