# app/services/loyalty_service.py
from app.repositories.loyalty_account_repository import (
    LoyaltyAccountRepository
)
from app.schemas.checkout import CheckoutResponseDto
from app.schemas.points import PointsDto


class LoyaltyService:
    """Service layer for handling loyalty-related operations."""

    def __init__(self, loyalty_account_repository: LoyaltyAccountRepository):
        """
        Initializes the LoyaltyService with a loyalty account repository.

        Args:
            loyalty_account_repository (LoyaltyAccountRepository): Repository
                for loyalty account operations.
        """
        self.loyalty_account_repository: LoyaltyAccountRepository = \
            loyalty_account_repository

    def checkout(self, customer_id: int) -> CheckoutResponseDto:
        """
        Processes a checkout transaction for a customer.

        Args:
            customer_id (int): The ID of the customer checking out.

        Returns:
            CheckoutResponseDto: DTO containing the results of the checkout.
        """
        result: dict = self.loyalty_account_repository.checkout_transaction(
            customer_id)

        return CheckoutResponseDto(
            total_points_earned=result['totalPointsEarned'],
            invalid_products=result['invalidProducts'],
            products_missing_category=result['productsMissingCategory'],
            point_earning_rules_missing=result['pointEarningRulesMissing'],
            success=(len(result['invalidProducts']) == 0 and
                     len(result['productsMissingCategory']) == 0 and
                     len(result['pointEarningRulesMissing']) == 0)
        )

    def get_customer_points(self, customer_id: int) -> PointsDto:
        """
        Retrieves the total loyalty points for a customer.

        Args:
            customer_id (int): The ID of the customer whose points are being
                retrieved.

        Returns:
            PointsDto: DTO containing the points information.

        Raises:
            ValueError: If the loyalty account is not found.
        """
        loyalty_account = self.loyalty_account_repository.find_by_customer_id(
            customer_id)
        if not loyalty_account:
            raise ValueError("Loyalty account not found")
        return PointsDto(points=loyalty_account.points)
