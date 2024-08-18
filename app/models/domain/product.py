# app/models/domain/product.py
from typing import Optional


class Product:
    """
    Represents a product in the domain model.

    This class encapsulates the core attributes of a product, including
    its identification, name, price, category, and optional image URL.

    Attributes:
        id (int): The unique identifier for the product.
        name (str): The name of the product.
        price (float): The price of the product.
        category_id (int): The identifier of the category this product
        belongs to.
        image_url (Optional[str]): The URL of the product's image,
            if available.
    """

    def __init__(
        self,
        id: int,
        name: str,
        price: float,
        category_id: int,
        image_url: Optional[str] = None
    ) -> None:
        """
        Initializes a new Product instance.

        Args:
            id (int): The unique identifier for the product.
            name (str): The name of the product.
            price (float): The price of the product.
            category_id (int): The identifier of the category this product
                belongs to.
            image_url (Optional[str]): The URL of the product's image.
                Defaults to None.
        """
        self.id: int = id
        self.name: str = name
        self.price: float = price
        self.category_id: int = category_id
        self.image_url: Optional[str] = image_url
