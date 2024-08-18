# app/serialization/product_serializer.py
from app.serialization.base_serializer import BaseSerializer
from app.schemas.product import (
    ProductCreateDto, ProductUpdateDto, ProductResponseDto
)


class ProductSerializer(BaseSerializer):
    @staticmethod
    def serialize_response(product: ProductResponseDto) -> dict:
        """
        Serializes a ProductResponseDto into a dictionary.

        Args:
            product (ProductResponseDto): The product response data.

        Returns:
            dict: The serialized product response.
        """
        return BaseSerializer.serialize(product)

    @staticmethod
    def deserialize_create(data: dict) -> ProductCreateDto:
        """
        Deserializes a dictionary into a ProductCreateDto.

        Args:
            data (dict): The data to deserialize.

        Returns:
            ProductCreateDto: The deserialized product creation data.
        """
        return BaseSerializer.deserialize(data, ProductCreateDto)

    @staticmethod
    def deserialize_update(data: dict) -> ProductUpdateDto:
        """
        Deserializes a dictionary into a ProductUpdateDto.

        Args:
            data (dict): The data to deserialize.

        Returns:
            ProductUpdateDto: The deserialized product update data.
        """
        return BaseSerializer.deserialize(data, ProductUpdateDto)
