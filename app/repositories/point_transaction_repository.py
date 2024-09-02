# app/repositories/point_transaction_repository.py

from typing import List
from datetime import datetime
from sqlalchemy import between
from app.repositories.base_repository import BaseRepository
from app.models.database.point_transaction import PointTransactionTable
from app.models.domain.point_transaction import PointTransaction
from app.mappers.point_transaction_mapper import PointTransactionMapper
from app import db


class PointTransactionRepository(BaseRepository[PointTransactionTable]):
    def __init__(self):
        """
        Initializes the PointTransactionRepository with
        the PointTransactionTable model.
        """
        super().__init__(PointTransactionTable)

    def create(self, transaction: PointTransaction) -> PointTransaction:
        """
        Creates a new point transaction in the repository.

        Args:
            transaction (PointTransaction): The PointTransaction object
                to create.

        Returns:
            PointTransaction: The created PointTransaction.
        """
        transaction_table = PointTransactionMapper.to_persistence(transaction)
        created_transaction = super().create(transaction_table)
        return PointTransactionMapper.to_domain(created_transaction)

    def find_by_loyalty_account_id(
        self, loyalty_account_id: int
    ) -> List[PointTransaction]:
        """
        Finds all point transactions associated with a specific
        loyalty account ID.

        Args:
            loyalty_account_id (int): The unique identifier of the
            loyalty account.

        Returns:
            List[PointTransaction]: A list of PointTransaction objects.
        """
        transaction_tables = db.session.query(PointTransactionTable).filter(
            PointTransactionTable.loyalty_account_id == loyalty_account_id
        ).all()
        return [
            PointTransactionMapper.to_domain(transaction)
            for transaction in transaction_tables
        ]

    def find_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[PointTransaction]:
        """
        Finds all point transactions within a specified date range.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.

        Returns:
            List[PointTransaction]: A list of PointTransaction objects.
        """
        transaction_tables = db.session.query(PointTransactionTable).filter(
            between(PointTransactionTable.transaction_date,
                    start_date, end_date)
        ).all()
        return [
            PointTransactionMapper.to_domain(transaction)
            for transaction in transaction_tables
        ]

    def find_by_id(self, id: int) -> PointTransaction:
        """
        Finds a point transaction by its ID.

        Args:
            id (int): The unique identifier of the point transaction.

        Returns:
            PointTransaction: The found PointTransaction or None if not found.
        """
        transaction_table = super().find_by_id(id)
        return (
            PointTransactionMapper.to_domain(transaction_table)
            if transaction_table
            else None
        )

    def update(self, transaction: PointTransaction) -> PointTransaction:
        """
        Updates an existing point transaction in the repository.

        Args:
            transaction (PointTransaction): The PointTransaction object
            to update.

        Returns:
            PointTransaction: The updated PointTransaction.
        """
        transaction_table = PointTransactionMapper.to_persistence(transaction)
        updated_transaction = super().update(transaction_table)
        return PointTransactionMapper.to_domain(updated_transaction)

    def delete(self, id: int) -> None:
        """
        Deletes a point transaction by its ID.

        Args:
            id (int): The unique identifier of the point transaction to delete.
        """
        super().delete(id)
