# app/serialization/base_serializer.py
from pydantic import BaseModel, ValidationError
from typing import Type, Any, Union, List


class BaseSerializer:
    @staticmethod
    def serialize(obj: Any) -> Union[dict, List[dict], Any]:
        """
        Serializes an object to a dictionary using Pydantic's BaseModel or
        recursively serializes a list of objects.

        Args:
            obj (Any): The object to serialize.

        Returns:
            Union[dict, List[dict], Any]: The serialized object,
            or the original object if not a BaseModel or list.
        """
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        elif isinstance(obj, list):
            return [BaseSerializer.serialize(item) for item in obj]
        else:
            return obj

    @staticmethod
    def deserialize(data: dict, model: Type[BaseModel]) -> BaseModel:
        """
        Deserializes a dictionary into a Pydantic BaseModel.

        Args:
            data (dict): The data to deserialize.
            model (Type[BaseModel]): The Pydantic model class to use for
            deserialization.

        Returns:
            BaseModel: An instance of the specified BaseModel.

        Raises:
            ValueError: If the data cannot be deserialized into the model.
        """
        try:
            return model(**data)
        except ValidationError as e:
            raise ValueError(str(e))
