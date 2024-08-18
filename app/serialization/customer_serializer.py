# app/serialization/customer_serializer.py
from app.serialization.base_serializer import BaseSerializer
from app.schemas.customer import (
    CustomerCreateDto,
    CustomerUpdateDto,
    CustomerResponseDto,
)


class CustomerSerializer(BaseSerializer):
    @staticmethod
    def serialize_response(customer: CustomerResponseDto) -> dict:
        """
        Serializes a CustomerResponseDto into a dictionary.

        Args:
            customer (CustomerResponseDto): The customer response data.

        Returns:
            dict: The serialized customer response.
        """
        return BaseSerializer.serialize(customer)

    @staticmethod
    def deserialize_create(data: dict) -> CustomerCreateDto:
        """
        Deserializes a dictionary into a CustomerCreateDto.

        Args:
            data (dict): The data to deserialize.

        Returns:
            CustomerCreateDto: The deserialized customer creation data.
        """
        return BaseSerializer.deserialize(data, CustomerCreateDto)

    @staticmethod
    def deserialize_update(data: dict) -> CustomerUpdateDto:
        """
        Deserializes a dictionary into a CustomerUpdateDto.

        Args:
            data (dict): The data to deserialize.

        Returns:
            CustomerUpdateDto: The deserialized customer update data.
        """
        return BaseSerializer.deserialize(data, CustomerUpdateDto)
