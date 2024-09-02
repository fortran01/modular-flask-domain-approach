# app/mappers/base_mapper.py

from typing import TypeVar, Generic, Dict, Any, List, Union

T = TypeVar('T')


class BaseMapper(Generic[T]):
    """
    A base class for mappers that provides common functionality for mapping
    between different representations of data.

    This class is designed to be subclassed by specific entity mappers.
    """

    @staticmethod
    def to_dict(obj: Any) -> Dict[str, Any]:
        """
        Convert an object to a dictionary.

        Args:
            obj (Any): The object to convert.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        if hasattr(obj, '__dict__'):
            return {k: v for k, v in obj.__dict__.items()
                    if not k.startswith('_')}
        return dict(obj)

    @classmethod
    def to_domain(cls, data: Dict[str, Any]) -> T:
        """
        Convert a dictionary to a domain model instance.

        This method should be overridden by subclasses to provide
        entity-specific mapping logic.

        Args:
            data (Dict[str, Any]): The dictionary containing the data.

        Returns:
            T: An instance of the domain model.

        Raises:
            NotImplementedError: If the method is not overridden by a subclass.
        """
        raise NotImplementedError("Subclasses must implement to_domain method")

    @classmethod
    def to_dto(cls, domain_model: T) -> Dict[str, Any]:
        """
        Convert a domain model instance to a DTO (Data Transfer Object).

        This method should be overridden by subclasses to provide
        entity-specific mapping logic.

        Args:
            domain_model (T): The domain model instance.

        Returns:
            Dict[str, Any]: A dictionary representing the DTO.

        Raises:
            NotImplementedError: If the method is not overridden by a subclass.
        """
        raise NotImplementedError("Subclasses must implement to_dto method")

    @classmethod
    def to_persistence(cls, domain_model: T) -> Dict[str, Any]:
        """
        Convert a domain model instance to a format suitable for persistence.

        This method should be overridden by subclasses to provide
        entity-specific mapping logic.

        Args:
            domain_model (T): The domain model instance.

        Returns:
            Dict[str, Any]: A dictionary representing the persistence model.

        Raises:
            NotImplementedError: If the method is not overridden by a subclass.
        """
        raise NotImplementedError(
            "Subclasses must implement to_persistence method")

    @classmethod
    def map_list(cls, items: List[Union[Dict[str, Any], T]],
                 mapping_method: str) -> List[Union[Dict[str, Any], T]]:
        """
        Map a list of items using the specified mapping method.

        Args:
            items (List[Union[Dict[str, Any], T]]): The list of items to map.
            mapping_method (str): The name of the mapping method to use
                                  ('to_domain', 'to_dto', or 'to_persistence').

        Returns:
            List[Union[Dict[str, Any], T]]: A list of mapped items.

        Raises:
            ValueError: If an invalid mapping_method is provided.
        """
        if mapping_method not in ['to_domain', 'to_dto', 'to_persistence']:
            raise ValueError("Invalid mapping method")

        mapper_method = getattr(cls, mapping_method)
        return [mapper_method(item) for item in items]
