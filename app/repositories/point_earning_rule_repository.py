# app/repositories/point_earning_rule_repository.py

from typing import List, Optional
from datetime import date
from sqlalchemy import and_, or_
from app.repositories.base_repository import BaseRepository
from app.models.database.point_earning_rule import PointEarningRuleTable
from app.models.domain.point_earning_rule import PointEarningRule
from app.mappers.point_earning_rule_mapper import PointEarningRuleMapper
from app import db


class PointEarningRuleRepository(BaseRepository[PointEarningRuleTable]):
    def __init__(self):
        """
        Initializes the PointEarningRuleRepository with the
        PointEarningRuleTable model.
        """
        super().__init__(PointEarningRuleTable)

    def find_by_id(self, id: int) -> Optional[PointEarningRule]:
        """
        Finds a point earning rule by its ID.

        Args:
            id (int): The unique identifier of the point earning rule.

        Returns:
            Optional[PointEarningRule]: The found point earning rule
                or None if not found.
        """
        rule_table = super().find_by_id(id)
        return (
            PointEarningRuleMapper.to_domain(rule_table)
            if rule_table
            else None
        )

    def find_active_rule_for_category(
        self, category_id: int, date: date
    ) -> Optional[PointEarningRule]:
        """
        Finds an active point earning rule for a specific category
        on a given date.

        Args:
            category_id (int): The unique identifier of the category.
            date (date): The date to check for an active rule.

        Returns:
            Optional[PointEarningRule]: The active point earning rule
            or None if no active rule is found.
        """
        rule_table = db.session.query(PointEarningRuleTable).filter(
            and_(
                PointEarningRuleTable.category_id == category_id,
                PointEarningRuleTable.start_date <= date,
                or_(
                    PointEarningRuleTable.end_date.is_(None),
                    PointEarningRuleTable.end_date >= date
                )
            )
        ).first()
        return (
            PointEarningRuleMapper.to_domain(rule_table)
            if rule_table
            else None
        )

    def create(self, rule: PointEarningRule) -> PointEarningRule:
        """
        Creates a new point earning rule.

        Args:
            rule (PointEarningRule): The point earning rule object to create.

        Returns:
            PointEarningRule: The created PointEarningRule object.
        """
        rule_table = PointEarningRuleMapper.to_persistence(rule)
        created_rule = super().create(rule_table)
        return PointEarningRuleMapper.to_domain(created_rule)

    def update(self, rule: PointEarningRule) -> PointEarningRule:
        """
        Updates an existing point earning rule.

        Args:
            rule (PointEarningRule): The point earning rule object to update.

        Returns:
            PointEarningRule: The updated PointEarningRule object.
        """
        rule_table = PointEarningRuleMapper.to_persistence(rule)
        updated_rule = super().update(rule_table)
        return PointEarningRuleMapper.to_domain(updated_rule)

    def delete(self, id: int) -> None:
        """
        Deletes a point earning rule by its ID.

        Args:
            id (int): The unique identifier of the point earning rule
                to delete.
        """
        super().delete(id)

    def find_by_category(self, category_id: int) -> List[PointEarningRule]:
        """
        Finds point earning rules by category ID.

        Args:
            category_id (int): The unique identifier of the category.

        Returns:
            List[PointEarningRule]: A list of PointEarningRule objects.
        """
        rule_tables = db.session.query(PointEarningRuleTable).filter(
            PointEarningRuleTable.category_id == category_id
        ).all()
        return [PointEarningRuleMapper.to_domain(rule) for rule in rule_tables]
