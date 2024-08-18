from __future__ import annotations
from app import db
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.database.category import CategoryTable


class PointEarningRuleTable(db.Model):
    """
    Represents a point earning rule in the database.

    This model defines the structure of the 'point_earning_rules' table
    in the database, including fields for rule identification, associated
    category, points per dollar, start and end dates, and timestamps for
    record creation and updates.

    Attributes:
        id (int): The primary key of the point earning rule record.
        category_id (int): The foreign key referencing the associated
            category's id.
        points_per_dollar (int): The number of points earned per dollar spent.
        start_date (date): The date when the rule becomes effective.
        end_date (Optional[date]): The date when the rule expires,
        if applicable.
        created_at (datetime): The timestamp when the rule record was created.
        updated_at (datetime): The timestamp when the rule record
        was last updated.
        category (CategoryTable): The category associated with this
        point earning rule.
    """

    __tablename__: str = 'point_earning_rules'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    category_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    points_per_dollar: Mapped[int] = db.Column(db.Integer, nullable=False)
    start_date: Mapped[date] = db.Column(db.Date, nullable=False)
    end_date: Mapped[Optional[date]] = db.Column(db.Date)
    created_at: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category: Mapped["CategoryTable"] = relationship(
        "CategoryTable", back_populates='point_earning_rules')
