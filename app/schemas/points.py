# app/schemas/points.py
from pydantic import BaseModel


class PointsDto(BaseModel):
    """
    Data Transfer Object for representing the points of a loyalty account.

    Attributes:
        points (int): The total number of loyalty points.
    """
    points: int
