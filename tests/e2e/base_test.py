# tests/e2e/base_test.py

import unittest
from app import create_app
from app import db as _db
from config.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        _db.create_all()

    def tearDown(self):
        _db.session.remove()
        _db.drop_all()
        self.app_context.pop()

    def create_app(self):
        return create_app(TestConfig)

    def list_routes(self):
        """Prints out all routes defined in the application."""
        with self.app.app_context():
            for rule in self.app.url_map.iter_rules():
                methods = ','.join(sorted(rule.methods))
                print(f"{rule.endpoint}: {rule.rule} [{methods}]")
