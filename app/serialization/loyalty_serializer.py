# app/serialization/loyalty_serializer.py
from app.serialization.base_serializer import BaseSerializer
from app.schemas.checkout import CheckoutResponseDto
from app.schemas.points import PointsDto


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
