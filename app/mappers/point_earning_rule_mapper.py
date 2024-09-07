# app/mappers/point_earning_rule_mapper.py

from typing import Dict, Any, List
from datetime import date
from app.mappers.base_mapper import BaseMapper
from app.models.domain.point_earning_rule import PointEarningRule
from app.models.database.point_earning_rule import PointEarningRuleTable
from app.schemas.point_earning_rule import (
    PointEarningRuleCreateDto,
    PointEarningRuleResponseDto
)
from app.mappers.category_mapper import CategoryMapper


class PointEarningRuleMapper(BaseMapper[PointEarningRule]):
    """
    Mapper class for the PointEarningRule entity. Handles conversions between
    domain model, database model, and DTOs.
    """

    @classmethod
    def to_domain(cls, data: Dict[str, Any]) -> PointEarningRule:
        """
        Convert a dictionary to a PointEarningRule domain model instance.

        Args:
            data (Dict[str, Any]): The dictionary containing point earning
                rule data.

        Returns:
            PointEarningRule: An instance of the PointEarningRule domain model.
        """
        return PointEarningRule(
            id=data.get('id'),
            category=CategoryMapper.to_domain(
                data['category']) if data.get('category') else None,
            category_id=data['category_id'],
            points_per_dollar=data['points_per_dollar'],
            start_date=data['start_date'],
            end_date=data.get('end_date')
        )

    @classmethod
    def to_dto(cls, domain_model: PointEarningRule) -> PointEarningRuleResponseDto:  # noqa: E501
        """
        Convert a PointEarningRule domain model instance to a
        PointEarningRuleResponseDto.

        Args:
            domain_model (PointEarningRule): The PointEarningRule
                domain model instance.

        Returns:
            PointEarningRuleResponseDto: A DTO representing the
              point earning rule.
        """
        return PointEarningRuleResponseDto(
            id=domain_model.id,
            category_id=domain_model.category_id,
            points_per_dollar=domain_model.points_per_dollar,
            start_date=domain_model.start_date,
            end_date=domain_model.end_date
        )

    @classmethod
    def from_create_dto(cls, dto: PointEarningRuleCreateDto) -> PointEarningRule:  # noqa: E501
        """
        Create a PointEarningRule domain model instance from
        a PointEarningRuleCreateDto.

        Args:
            dto (PointEarningRuleCreateDto): The DTO containing data for
            creating a point earning rule.

        Returns:
            PointEarningRule: A new instance of the PointEarningRule
            domain model.
        """
        return PointEarningRule(
            id=None,  # ID will be assigned by the database
            category=None,  # Category will be set separately
            category_id=dto.category_id,
            points_per_dollar=dto.points_per_dollar,
            start_date=dto.start_date,
            end_date=dto.end_date
        )

    @classmethod
    def from_persistence(cls, db_model: PointEarningRuleTable) -> PointEarningRule:  # noqa: E501
        """
        Convert a PointEarningRuleTable database model to a PointEarningRule
        domain model.

        Args:
            db_model (PointEarningRuleTable): The database model instance.

        Returns:
            PointEarningRule: An instance of the PointEarningRule domain model.
        """
        return PointEarningRule(
            id=db_model.id,
            category=CategoryMapper.from_persistence(
                db_model.category) if db_model.category else None,
            category_id=db_model.category_id,
            points_per_dollar=db_model.points_per_dollar,
            start_date=db_model.start_date,
            end_date=db_model.end_date
        )

    @classmethod
    def to_persistence_model(cls, domain_model: PointEarningRule) -> PointEarningRuleTable:  # noqa: E501
        """
        Convert a PointEarningRule domain model to a PointEarningRuleTable
        database model.

        Args:
            domain_model (PointEarningRule): The PointEarningRule
            domain model instance.

        Returns:
            PointEarningRuleTable: An instance of the PointEarningRuleTable
                database model.
        """
        return PointEarningRuleTable(
            id=domain_model.id,
            category_id=domain_model.category_id,
            points_per_dollar=domain_model.points_per_dollar,
            start_date=domain_model.start_date,
            end_date=domain_model.end_date
        )

    @classmethod
    def map_domain_list(cls, rules: List[PointEarningRule]) -> List[PointEarningRuleResponseDto]:  # noqa: E501
        """
        Map a list of PointEarningRule domain models to a list of
        PointEarningRuleResponseDto.

        Args:
            rules (List[PointEarningRule]): A list of PointEarningRule
            domain models.

        Returns:
            List[PointEarningRuleResponseDto]: A list of
                PointEarningRuleResponseDto instances.
        """
        return [cls.to_dto(rule) for rule in rules]

    @classmethod
    def find_active_rule(cls, rules: List[PointEarningRule], current_date: date) -> PointEarningRule:  # noqa: E501
        """
        Find the active rule from a list of PointEarningRule domain models fo
        a given date.

        Args:
            rules (List[PointEarningRule]): A list of PointEarningRule
                domain models.
            current_date (date): The date to check for active rules.

        Returns:
            PointEarningRule: The active PointEarningRule for the given date,
                or None if no active rule is found.
        """
        for rule in rules:
            if rule.start_date <= current_date and \
                    (rule.end_date is None or rule.end_date >= current_date):
                return rule
        return None
