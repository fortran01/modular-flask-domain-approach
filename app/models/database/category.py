# app/models/database/category.py
from app import db
from datetime import datetime
from typing import List
from app.models.database.product import ProductTable
from app.models.database.point_earning_rule import PointEarningRuleTable


class CategoryTable(db.Model):
    """
    Represents a category in the database.

    This model defines the structure of the 'categories' table in the database,
    including fields for category identification, name, and timestamps for
    record creation and updates.

    Attributes:
        id (int): The primary key of the category record.
        name (str): The name of the category, limited to 50 characters.
        created_at (datetime): The timestamp when the category record
            was created.
        updated_at (datetime): The timestamp when the category record
            was last updated.
        products (List[ProductTable]): The list of products associated with
            this category.
        point_earning_rules (List[PointEarningRuleTable]): The list of point
            earning rules associated with this category.
    """

    __tablename__: str = 'categories'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    products: List[ProductTable] = db.relationship(
        'ProductTable', back_populates='category')
    point_earning_rules: List[PointEarningRuleTable] = db.relationship(
        'PointEarningRuleTable', back_populates='category')
