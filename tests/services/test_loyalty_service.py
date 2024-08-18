# app/tests/services/test_loyalty_service.py
import pytest
from unittest.mock import Mock
from app.services.loyalty_service import LoyaltyService
from app.models.domain.loyalty_account import LoyaltyAccount
from app.schemas.checkout import CheckoutResponseDto
from app.schemas.points import PointsDto


@pytest.fixture
def loyalty_service():
    mock_loyalty_account_repository = Mock()
    return LoyaltyService(mock_loyalty_account_repository)


def test_checkout(customer_id=1):
    # Arrange
    mock_loyalty_account_repository = Mock()
    loyalty_service = LoyaltyService(mock_loyalty_account_repository)
    mock_result = {
        'totalPointsEarned': 100,
        'invalidProducts': [],
        'productsMissingCategory': [],
        'pointEarningRulesMissing': []
    }
    mock_loyalty_account_repository.checkout_transaction.return_value = \
        mock_result

    # Act
    result = loyalty_service.checkout(customer_id)

    # Assert
    assert isinstance(result, CheckoutResponseDto)
    assert result.total_points_earned == 100
    assert result.success is True
    mock_loyalty_account_repository.checkout_transaction. \
        assert_called_once_with(customer_id)


def test_get_customer_points_existing_account(customer_id=1):
    # Arrange
    mock_loyalty_account_repository = Mock()
    loyalty_service = LoyaltyService(mock_loyalty_account_repository)
    mock_loyalty_account = LoyaltyAccount(
        id=1, customer_id=customer_id, points=150)
    mock_loyalty_account_repository.find_by_customer_id.return_value = \
        mock_loyalty_account

    # Act
    result = loyalty_service.get_customer_points(customer_id)

    # Assert
    assert isinstance(result, PointsDto)
    assert result.points == 150
    mock_loyalty_account_repository.find_by_customer_id. \
        assert_called_once_with(customer_id)


def test_get_customer_points_non_existing_account(customer_id=999):
    # Arrange
    mock_loyalty_account_repository = Mock()
    loyalty_service = LoyaltyService(mock_loyalty_account_repository)
    mock_loyalty_account_repository.find_by_customer_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Loyalty account not found"):
        loyalty_service.get_customer_points(customer_id)
    mock_loyalty_account_repository.find_by_customer_id. \
        assert_called_once_with(customer_id)
