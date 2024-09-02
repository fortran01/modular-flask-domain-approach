# app/repositories/category_repository.py
from typing import List, Optional
from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.models.database.category import CategoryTable
from app.models.domain.category import Category
from app.mappers.category_mapper import CategoryMapper
from app import db


class CategoryRepository(BaseRepository[CategoryTable]):
    def __init__(self) -> None:
        """
        Initializes the CategoryRepository with the CategoryTable model.
        """
        super().__init__(CategoryTable)

    def find_by_id(self, id: int) -> Optional[Category]:
        category_table = super().find_by_id(id)
        return CategoryMapper.to_domain(category_table) \
            if category_table else None

    def find_all(self) -> List[Category]:
        category_tables = super().find_all()
        return [CategoryMapper.to_domain(cat) for cat in category_tables]

    def find_with_active_rule(self, date: str) -> List[Category]:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        category_tables = db.session.query(CategoryTable).join(
            CategoryTable.point_earning_rules
        ).filter(
            CategoryTable.point_earning_rules.any(
                db.and_(
                    CategoryTable.point_earning_rules.start_date <= date_obj,
                    db.or_(
                        CategoryTable.point_earning_rules.end_date.is_(None),
                        CategoryTable.point_earning_rules.end_date >= date_obj
                    )
                )
            )
        ).all()
        return [CategoryMapper.to_domain(cat) for cat in category_tables]

    def create(self, category: Category) -> Category:
        category_table = CategoryMapper.to_persistence(category)
        created_category = super().create(category_table)
        return CategoryMapper.to_domain(created_category)

    def update(self, category: Category) -> Category:
        category_table = CategoryMapper.to_persistence(category)
        updated_category = super().update(category_table)
        return CategoryMapper.to_domain(updated_category)

    def delete(self, id: int) -> None:
        super().delete(id)
