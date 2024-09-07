# tests/e2e/test_product_e2e.py

import json
from tests.e2e.base_test import BaseTestCase
from app.models.database.product import ProductTable
from app.models.database.category import CategoryTable
from app.schemas.product import ProductCreateDto, ProductUpdateDto
from app.mappers.product_mapper import ProductMapper
from app import db


class TestProductE2E(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a test category
        self.category = CategoryTable(name="Test Category")
        db.session.add(self.category)
        db.session.commit()

        # Create a test customer for authentication
        self.client.set_cookie('customer_id', '1')

    def test_create_product(self):
        # Arrange
        product_data = ProductCreateDto(
            name="Test Product",
            price=99.99,
            category_id=self.category.id,
            image_url="http://example.com/test.jpg"
        )

        # Act
        response = self.client.post('/products',
                                    data=json.dumps(product_data.dict()),
                                    content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn('id', data)
        self.assertEqual(data['name'], "Test Product")
        self.assertEqual(data['price'], 99.99)
        self.assertEqual(data['category_id'], self.category.id)
        self.assertEqual(data['image_url'], "http://example.com/test.jpg")

        # Verify database state
        product = ProductTable.query.filter_by(name="Test Product").first()
        self.assertIsNotNone(product)
        self.assertEqual(product.price, 99.99)

    def test_get_product(self):
        # Arrange
        product_dto = ProductCreateDto(
            name="Existing Product",
            price=49.99,
            category_id=self.category.id,
            image_url="http://example.com/existing.jpg"
        )
        product = ProductMapper.from_create_dto(product_dto)
        db.session.add(ProductMapper.to_persistence_model(product))
        db.session.commit()
        product_from_db = ProductTable.query.filter_by(
            name="Existing Product").first()

        # Act
        response = self.client.get(f'/products/{product_from_db.id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['name'], "Existing Product")
        self.assertEqual(data['price'], 49.99)
        self.assertEqual(data['category_id'], self.category.id)
        self.assertEqual(data['image_url'], "http://example.com/existing.jpg")

    def test_update_product(self):
        # Arrange
        product_dto = ProductCreateDto(
            name="Product to Update",
            price=79.99,
            category_id=self.category.id,
            image_url="http://example.com/update.jpg"
        )
        product = ProductMapper.from_create_dto(product_dto)
        db.session.add(ProductMapper.to_persistence_model(product))
        db.session.commit()
        product_from_db = ProductTable.query.filter_by(
            name="Product to Update").first()

        update_data = ProductUpdateDto(
            name="Updated Product",
            price=89.99
        )

        # Act
        response = self.client.put(f'/products/{product_from_db.id}',
                                   data=json.dumps(update_data.model_dump()),
                                   content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['name'], "Updated Product")
        self.assertEqual(data['price'], 89.99)

        # Verify database state
        updated_product = ProductTable.query.get(product_from_db.id)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.price, 89.99)

    def test_delete_product(self):
        # Arrange
        product_dto = ProductCreateDto(
            name="Product to Delete",
            price=29.99,
            category_id=self.category.id,
            image_url="http://example.com/delete.jpg"
        )
        product = ProductMapper.from_create_dto(product_dto)
        db.session.add(ProductMapper.to_persistence_model(product))
        db.session.commit()
        product_from_db = ProductTable.query.filter_by(
            name="Product to Delete").first()

        # Act
        response = self.client.delete(f'/products/{product_from_db.id}')

        # Assert
        self.assertEqual(response.status_code, 204)

        # Verify database state
        deleted_product = ProductTable.query.get(product_from_db.id)
        self.assertIsNone(deleted_product)

    def test_get_all_products(self):
        # Arrange
        product1 = ProductTable(
            name="Product 1", price=10.99, category_id=self.category.id)
        product2 = ProductTable(
            name="Product 2", price=20.99, category_id=self.category.id)
        db.session.add_all([product1, product2])
        db.session.commit()

        # Act
        response = self.client.get('/products')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Product 1")
        self.assertEqual(data[1]['name'], "Product 2")
