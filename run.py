# run.py
import sys
from app import create_app, db
from app.database.seeder import DatabaseSeeder
from flask import Flask

app: Flask = create_app()

if __name__ == '__main__':
    with app.app_context():
        if len(sys.argv) > 1 and sys.argv[1] == 'seed':
            seeder = DatabaseSeeder(db)
            seeder.seed()
            print("Database seeded successfully")
        else:
            """
            Entry point of the application.

            This script creates a Flask application instance and runs it in
            debug mode when executed directly. The application is only run
            if this script is the main program and no 'seed' argument is
            provided.

            The debug mode is set to True, which enables features like
            automatic reloading on code changes and detailed error pages.
            This should be set to False in a production environment.
            """
            app.run(debug=True)
