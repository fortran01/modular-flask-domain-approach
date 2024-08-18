# app/di_container.py
from typing import Dict, Any
from flask import g


class DIContainer:
    """Dependency Injection container for managing dependencies."""

    def __init__(self) -> None:
        """Initialize DIContainer with an empty dependencies dict."""
        self._dependencies: Dict[str, Any] = {}

    def register(self, name: str, dependency: Any) -> None:
        """
        Register a dependency.

        Args:
            name (str): The name identifier for the dependency.
            dependency (Any): The dependency instance.
        """
        self._dependencies[name] = dependency

    def resolve(self, name: str) -> Any:
        """
        Resolve a dependency by name.

        Args:
            name (str): The name identifier for the dependency.

        Returns:
            Any: The resolved dependency or None if not found.
        """
        return self._dependencies.get(name)


# Create a global instance of the container
container = DIContainer()

# Dependency registration function


def register_dependencies(app):
    """
    Register all dependencies into the DIContainer and attach it to the app.

    Args:
        app: The Flask application instance.
    """
    from app.repositories.customer_repository import CustomerRepository
    from app.repositories.loyalty_account_repository import (
        LoyaltyAccountRepository
    )
    from app.repositories.product_repository import ProductRepository
    from app.repositories.category_repository import CategoryRepository
    from app.repositories.shopping_cart_repository import (
        ShoppingCartRepository
    )
    from app.services.customer_service import CustomerService
    from app.services.loyalty_service import LoyaltyService
    from app.services.product_service import ProductService
    from app.services.shopping_cart_service import ShoppingCartService

    # Register repositories
    container.register('customer_repository', CustomerRepository())
    container.register('loyalty_account_repository',
                       LoyaltyAccountRepository())
    container.register('product_repository', ProductRepository())
    container.register('category_repository', CategoryRepository())
    container.register('shopping_cart_repository', ShoppingCartRepository())

    # Register services
    container.register('customer_service', CustomerService(
        container.resolve('customer_repository'),
        container.resolve('loyalty_account_repository')
    ))
    container.register('loyalty_service', LoyaltyService(
        container.resolve('loyalty_account_repository')
    ))
    container.register('product_service', ProductService(
        container.resolve('product_repository'),
        container.resolve('category_repository')
    ))
    container.register('shopping_cart_service', ShoppingCartService(
        container.resolve('shopping_cart_repository'),
        container.resolve('product_repository')
    ))

    # Add the container to the app context
    @app.before_request
    def before_request():
        """Attach the DIContainer to the global object before each request."""
        g.container = container
