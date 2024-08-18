import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for the Flask application.

    This class defines configuration variables used throughout the application.
    It loads environment variables and sets default values where necessary.

    Attributes:
        SECRET_KEY (str): A secret key used for securely signing data.
        SQLALCHEMY_DATABASE_URI (str): The URI for the database connection.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to enable/disable
        SQLAlchemy modification tracking.
    """

    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + \
        os.path.join(os.path.abspath(
            os.path.dirname(__file__)), '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
