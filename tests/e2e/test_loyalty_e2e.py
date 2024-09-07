# tests/e2e/test_loyalty_e2e.py

import json
from datetime import date
from tests.e2e.base_test import BaseTestCase
from app.models.database.customer import CustomerTable
from app.models.database.loyalty_account import LoyaltyAccountTable
from app.models.database.product import ProductTable
from app.models.database.shopping_cart import (
    ShoppingCartTable,
    ShoppingCartItemTable
)
from app import db
from app.models.database.category import CategoryTable
from app.models.database.point_earning_rule import PointEarningRuleTable


class TestLoyaltyE2E(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create categories
        self.default_category = CategoryTable(name="Default")
        self.electronics_category = CategoryTable(name="Electronics")
        self.books_category = CategoryTable(name="Books")
        db.session.add_all([
            self.default_category,
            self.electronics_category,
            self.books_category
        ])
        db.session.commit()

        # Create a test customer and products
        self.customer = CustomerTable(
            name="Test Customer", email="test@example.com")
        db.session.add(self.customer)
        self.product1 = ProductTable(
            name="Laptop",
            price=1200,
            category_id=self.electronics_category.id
        )
        self.product2 = ProductTable(
            name="Book", price=15.99, category_id=self.books_category.id)
        db.session.add_all([self.product1, self.product2])
        db.session.commit()

        # Create a loyalty account for the test customer
        self.loyalty_account = LoyaltyAccountTable(
            customer_id=self.customer.id, points=0)
        db.session.add(self.loyalty_account)
        db.session.commit()

        # Seed point earning rules
        today = date.today()
        next_year = today.replace(year=today.year + 1)

        rules = [
            PointEarningRuleTable(
                category_id=self.default_category.id,
                points_per_dollar=1,
                start_date=date(1900, 1, 1),
                end_date=date(2099, 12, 31)
            ),
            PointEarningRuleTable(
                category_id=self.electronics_category.id,
                points_per_dollar=2,
                start_date=today,
                end_date=next_year
            ),
            PointEarningRuleTable(
                category_id=self.books_category.id,
                points_per_dollar=1,
                start_date=today,
                end_date=next_year
            )
        ]
        db.session.add_all(rules)
        db.session.commit()

    def test_login(self):
        # Arrange
        login_data = {"customer_id": str(self.customer.id)}

        # Act
        response = self.client.post('/login',
                                    data=json.dumps(login_data),
                                    content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['success'])
        cookies = response.headers.get('Set-Cookie')
        self.assertIn('customer_id', cookies)

    def test_logout(self):
        # Arrange
        self.client.set_cookie('customer_id', str(
            self.customer.id), domain='localhost')

        # Act
        response = self.client.get('/logout')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['success'])
        # Check if the 'customer_id' cookie is set to be deleted
        set_cookie_header = response.headers.get('Set-Cookie')
        self.assertIn('customer_id', set_cookie_header)
        # This indicates the cookie is set to expire immediately
        self.assertIn('Max-Age=0', set_cookie_header)

    def test_checkout(self):
        # Arrange
        self.client.set_cookie('customer_id', str(self.customer.id))
        cart = ShoppingCartTable(customer_id=self.customer.id)
        db.session.add(cart)
        cart_from_db = db.session.query(ShoppingCartTable).filter_by(
            customer_id=self.customer.id).first()
        cart_item1 = ShoppingCartItemTable(
            cart_id=cart_from_db.id, product_id=self.product1.id, quantity=1)
        cart_item2 = ShoppingCartItemTable(
            cart_id=cart_from_db.id, product_id=self.product2.id, quantity=2)
        db.session.add_all([cart_item1, cart_item2])
        db.session.commit()

        # Act
        response = self.client.post('/checkout')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        print(data)
        self.assertIn('total_points_earned', data)
        self.assertTrue(data['success'])

        # Calculate expected points
        # (Laptop price * 2 points) + (Book price * 2 quantity * 1 point)
        expected_points = (1200 * 2) + (15.99 * 2 * 1)
        expected_points = int(expected_points)  # Round down to nearest integer

        # Verify loyalty points were added correctly
        updated_loyalty_account = LoyaltyAccountTable.query.filter_by(
            customer_id=self.customer.id).first()
        self.assertEqual(updated_loyalty_account.points, expected_points)
        self.assertEqual(data['total_points_earned'], expected_points)

        # Verify cart was cleared after checkout
        cart_items = ShoppingCartItemTable.query.filter_by(
            cart_id=cart.id).all()
        self.assertEqual(len(cart_items), 0)

    def test_get_points(self):
        # Arrange
        self.client.set_cookie('customer_id', str(self.customer.id))
        self.loyalty_account.points = 100
        db.session.commit()

        # Act
        response = self.client.get('/points')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['points'], 100)

    def test_add_to_cart(self):
        # Arrange
        self.client.set_cookie('customer_id', str(self.customer.id))
        cart_data = {
            "product_id": self.product1.id,
            "quantity": 2
        }

        # Act
        response = self.client.post('/cart',
                                    data=json.dumps(cart_data),
                                    content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['success'])

        # Verify cart item was added
        cart = ShoppingCartTable.query.filter_by(
            customer_id=self.customer.id).first()
        self.assertIsNotNone(cart)
        cart_item = ShoppingCartItemTable.query.filter_by(
            cart_id=cart.id, product_id=self.product1.id).first()
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.quantity, 2)

    def test_get_cart(self):
        # Arrange
        self.client.set_cookie('customer_id', str(self.customer.id))
        cart = ShoppingCartTable(customer_id=self.customer.id)
        db.session.add(cart)
        cart_from_db = db.session.query(ShoppingCartTable).filter_by(
            customer_id=self.customer.id).first()
        cart_item = ShoppingCartItemTable(
            cart_id=cart_from_db.id, product_id=self.product1.id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()

        # Act
        response = self.client.get('/cart')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['product']['id'], self.product1.id)
        self.assertEqual(data['items'][0]['quantity'], 1)

    def test_update_cart_item(self):
        # Arrange
        self.client.set_cookie('customer_id', str(self.customer.id))
        cart = ShoppingCartTable(customer_id=self.customer.id)
        db.session.add(cart)
        cart_from_db = db.session.query(ShoppingCartTable).filter_by(
            customer_id=self.customer.id).first()
        cart_item = ShoppingCartItemTable(
            cart_id=cart_from_db.id, product_id=self.product1.id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()

        update_data = {"quantity": 3}

        # Act
        response = self.client.put(f'/cart/{self.product1.id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['success'])

        # Verify cart item was updated
        updated_cart_item = ShoppingCartItemTable.query.filter_by(
            cart_id=cart.id, product_id=self.product1.id).first()
        self.assertEqual(updated_cart_item.quantity, 3)

    def test_remove_from_cart(self):
        # Arrange
        self.client.set_cookie('customer_id', str(self.customer.id))
        cart = ShoppingCartTable(customer_id=self.customer.id)
        db.session.add(cart)
        cart_from_db = db.session.query(ShoppingCartTable).filter_by(
            customer_id=self.customer.id).first()
        cart_item = ShoppingCartItemTable(
            cart_id=cart_from_db.id, product_id=self.product1.id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()

        # Act
        response = self.client.delete(f'/cart/{self.product1.id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['success'])

        # Verify cart item was removed
        removed_cart_item = ShoppingCartItemTable.query.filter_by(
            cart_id=cart.id, product_id=self.product1.id).first()
        self.assertIsNone(removed_cart_item)

    def test_clear_cart(self):
        # Arrange
        self.client.set_cookie('customer_id', str(self.customer.id))
        cart = ShoppingCartTable(customer_id=self.customer.id)
        db.session.add(cart)
        cart_from_db = db.session.query(ShoppingCartTable).filter_by(
            customer_id=self.customer.id).first()
        cart_item = ShoppingCartItemTable(
            cart_id=cart_from_db.id, product_id=self.product1.id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()

        # Act
        response = self.client.delete('/cart')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['success'])

        # Verify cart was cleared
        cart_items = ShoppingCartItemTable.query.filter_by(
            cart_id=cart.id).all()
        self.assertEqual(len(cart_items), 0)
