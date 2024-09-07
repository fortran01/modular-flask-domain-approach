# modular-flask-domain-approach

This project is a web-based loyalty program application built using Flask, a Python web framework. It demonstrates a modular approach to structuring a Flask application with domain-driven design principles. The application features a customer loyalty system where users can log in, view products, add items to a shopping cart, and earn points through purchases.

Key features include:

- User authentication system
- Product catalog display
- Shopping cart functionality
- Point system for customer loyalty
- Responsive frontend using Tailwind CSS
- RESTful API endpoints for various operations

The project showcases best practices in Flask development, including:

- Use of Flask-SQLAlchemy for database management
- Implementation of Flask-Migrate for database migrations
- Environment variable management with python-dotenv
- Data validation using Pydantic
- Testing setup with pytest

This modular approach allows for easier maintenance, scalability, and separation of concerns within the application architecture.

## Setup

- Clone the repository
- Activate the virtual environment

```bash
source venv/bin/activate
```

- Install the dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
FLASK_APP=app flask run
```

## Seeding the database

```bash
flask db init
flask db migrate
flask db upgrade
python run.py seed
```
