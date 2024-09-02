# tests/e2e/test_customer_e2e.py

import json
from tests.e2e.base_test import BaseTestCase
from app.models.database.customer import CustomerTable
from app.schemas.customer import CustomerCreateDto, CustomerUpdateDto
from app.mappers.customer_mapper import CustomerMapper
from app.models.domain.customer import Customer
from app import db


class TestCustomerE2E(BaseTestCase):
    def test_create_customer(self) -> None:
        """Test the creation of a customer via the API."""
        self.list_routes()
        # Arrange
        customer_data: CustomerCreateDto = CustomerCreateDto(
            name="John Doe",
            email="john@example.com"
        )

        # Act
        self.client.set_cookie('customer_id', '1')  # Set auth cookie
        response = self.client.post('/customers',
                                    data=json.dumps(
                                        customer_data.model_dump()),
                                    content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 201)
        data: dict = json.loads(response.data.decode())
        self.assertIn('id', data)
        self.assertEqual(data['name'], "John Doe")
        self.assertEqual(data['email'], "john@example.com")

        # Verify database state
        customer: CustomerTable = CustomerTable.query.filter_by(
            email="john@example.com").first()
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "John Doe")

    def test_get_customer(self) -> None:
        """Test retrieving a customer by ID via the API."""
        # Arrange
        customer_dto: CustomerCreateDto = CustomerCreateDto(
            name="Jane Doe", email="jane@example.com")
        customer: Customer = CustomerMapper.from_create_dto(customer_dto)
        customer_table: CustomerTable = CustomerMapper.to_persistence_model(
            customer)
        db.session.add(customer_table)
        db.session.commit()

        # Get the ID of the customer we just created
        customer_from_db = db.session.query(CustomerTable).filter_by(
            email="jane@example.com").first()
        self.assertIsNotNone(customer_from_db)
        self.assertEqual(customer_from_db.name, "Jane Doe")

        # Act
        self.client.set_cookie('customer_id', '1')  # Set auth cookie
        response = self.client.get(f'/customers/{customer_from_db.id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        data: dict = json.loads(response.data.decode())
        self.assertEqual(data['name'], "Jane Doe")
        self.assertEqual(data['email'], "jane@example.com")

    def test_update_customer(self) -> None:
        """Test updating a customer's information via the API."""
        # Arrange
        customer_dto: CustomerCreateDto = CustomerCreateDto(
            name="Bob Smith", email="bob@example.com")
        customer: Customer = CustomerMapper.from_create_dto(customer_dto)
        customer_table: CustomerTable = CustomerMapper.to_persistence_model(
            customer)
        db.session.add(customer_table)
        db.session.commit()

        # Get the ID of the customer we just created
        customer_from_db = db.session.query(CustomerTable).filter_by(
            email="bob@example.com").first()
        print(customer_from_db.id)
        self.assertIsNotNone(customer_from_db)
        self.assertEqual(customer_from_db.name, "Bob Smith")

        update_data: CustomerUpdateDto = CustomerUpdateDto(name="Robert Smith")

        # Act
        self.client.set_cookie('customer_id', '1')  # Set auth cookie
        response = self.client.put(f'/customers/{customer_from_db.id}',
                                   data=json.dumps(
                                       update_data.model_dump()),
                                   content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 200)
        data: dict = json.loads(response.data.decode())
        self.assertEqual(data['name'], "Robert Smith")
        self.assertEqual(data['email'], "bob@example.com")

        # Verify database state
        updated_customer: CustomerTable = db.session.query(CustomerTable).filter_by(  # noqa: E501
            id=customer_from_db.id).first()
        self.assertEqual(updated_customer.name, "Robert Smith")

    def test_delete_customer(self) -> None:
        """Test deleting a customer via the API."""
        # Arrange
        customer_dto: CustomerCreateDto = CustomerCreateDto(
            name="Alice Johnson", email="alice@example.com")
        customer: Customer = CustomerMapper.from_create_dto(customer_dto)
        customer_table: CustomerTable = CustomerMapper.to_persistence_model(
            customer)
        db.session.add(customer_table)
        db.session.commit()

        # Get the ID of the customer we just created
        customer_from_db = db.session.query(CustomerTable).filter_by(
            email="alice@example.com").first()
        self.assertIsNotNone(customer_from_db)
        self.assertEqual(customer_from_db.name, "Alice Johnson")

        # Act
        self.client.set_cookie('customer_id', '1')  # Set auth cookie
        response = self.client.delete(f'/customers/{customer_from_db.id}')

        # Assert
        self.assertEqual(response.status_code, 204)

        # Verify database state
        deleted_customer: CustomerTable = db.session.query(CustomerTable).filter_by(  # noqa: E501
            id=customer_from_db.id).first()
        self.assertIsNone(deleted_customer)
