# app/schemas/product_schema.py
from app.models.database.product import ProductTable
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class ProductSchema(SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Product data using
    Marshmallow-SQLAlchemy.

    Attributes:
        model (ProductTable): The database model to serialize.
        load_instance (bool): Whether to load an instance.
        include_fk (bool): Whether to include foreign keys.
    """
    class Meta:
        model: ProductTable = ProductTable
        load_instance: bool = True
        include_fk: bool = True


product_schema: ProductSchema = ProductSchema()
products_schema: ProductSchema = ProductSchema(many=True)
