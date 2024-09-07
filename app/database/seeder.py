# app/database/seeder.py

from typing import List
from app.models.database.category import CategoryTable
from app.models.database.product import ProductTable
from app.models.database.customer import CustomerTable
from app.models.database.loyalty_account import LoyaltyAccountTable
from app.models.database.point_earning_rule import PointEarningRuleTable
from app.models.database.shopping_cart import ShoppingCartTable
from datetime import date
from sqlalchemy.orm import Session


class DatabaseSeeder:
    """
    A class for seeding the database with initial data.
    """

    def __init__(self, db: Session):
        """
        Initialize the DatabaseSeeder.

        Args:
            db (Session): The database session to use for seeding.
        """
        self.db = db

    def seed(self) -> None:
        """
        Seed the database with initial data for all tables.
        """
        self.seed_categories()
        self.seed_products()
        self.seed_customers()
        self.seed_point_earning_rules()
        self.seed_shopping_carts()

    def seed_categories(self) -> None:
        """
        Seed the database with initial category data.
        """
        categories: List[CategoryTable] = [
            CategoryTable(name='Electronics'),
            CategoryTable(name='Books'),
            CategoryTable(name='Default')
        ]
        self.db.session.add_all(categories)
        self.db.session.commit()
        print("Categories seeded")

    def seed_products(self) -> None:
        """
        Seed the database with initial product data.
        """
        categories: List[CategoryTable] = CategoryTable.query.all()
        electronics: CategoryTable = next(
            cat for cat in categories if cat.name == 'Electronics')
        books: CategoryTable = next(
            cat for cat in categories if cat.name == 'Books')

        products: List[ProductTable] = [
            ProductTable(
                name='Laptop',
                price=1200.00,
                category=electronics,
                image_url='https://upload.wikimedia.org/wikipedia/commons/e/e9/Apple-desk-laptop-macbook-pro_%2823699397893%29.jpg'  # noqa: E501
            ),
            ProductTable(
                name='Science Fiction Book',
                price=15.99,
                category=books,
                image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Eric_Frank_Russell_-_Die_Gro%C3%9Fe_Explosion_-_Cover.jpg/770px-Eric_Frank_Russell_-_Die_Gro%C3%9Fe_Explosion_-_Cover.jpg'  # noqa: E501
            ),
        ]
        self.db.session.add_all(products)
        self.db.session.commit()
        print("Products seeded")

    def seed_customers(self) -> None:
        """
        Seed the database with initial customer and loyalty account data.
        """
        customers: List[CustomerTable] = [
            CustomerTable(name='John Doe', email='john.doe@example.com'),
            CustomerTable(name='Jane Smith', email='jane.smith@example.com'),
        ]
        self.db.session.add_all(customers)
        self.db.session.commit()

        for customer in customers:
            loyalty_account: LoyaltyAccountTable = LoyaltyAccountTable(
                customer_id=customer.id, points=100)
            self.db.session.add(loyalty_account)
        self.db.session.commit()
        print("Customers and Loyalty Accounts seeded")

    def seed_point_earning_rules(self) -> None:
        """
        Seed the database with initial point earning rule data.
        """
        categories: List[CategoryTable] = CategoryTable.query.all()
        default_category: CategoryTable = next(
            cat for cat in categories if cat.name == 'Default')
        electronics: CategoryTable = next(
            cat for cat in categories if cat.name == 'Electronics')
        books: CategoryTable = next(
            cat for cat in categories if cat.name == 'Books')

        today: date = date.today()
        next_year: date = today.replace(year=today.year + 1)

        rules: List[PointEarningRuleTable] = [
            PointEarningRuleTable(
                category=default_category,
                points_per_dollar=1,
                start_date=date(1900, 1, 1),
                end_date=date(2099, 12, 31)
            ),
            PointEarningRuleTable(
                category=electronics,
                points_per_dollar=2,
                start_date=today,
                end_date=next_year
            ),
            PointEarningRuleTable(
                category=books,
                points_per_dollar=1,
                start_date=today,
                end_date=next_year
            ),
        ]
        self.db.session.add_all(rules)
        self.db.session.commit()
        print("Point Earning Rules seeded")

    def seed_shopping_carts(self) -> None:
        """
        Seed the database with initial shopping cart data for each customer.
        """
        customers: List[CustomerTable] = CustomerTable.query.all()
        for customer in customers:
            cart: ShoppingCartTable = ShoppingCartTable(
                customer_id=customer.id)
            self.db.session.add(cart)
        self.db.session.commit()
        print("Shopping Carts seeded")
