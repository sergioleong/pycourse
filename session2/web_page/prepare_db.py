import argparse
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def prepare_database(db_name, schema_file):
    """
    Creates or initializes a SQLite database using SQLAlchemy,
    executing SQL commands from a specified schema file.

    Args:
        db_name (str): The name of the SQLite database file (e.g., 'database.db').
        schema_file (str): The path to the SQL schema file (e.g., 'schema.sql').
    """
    # Define the database URL. For SQLite, it's 'sqlite:///path/to/database.db'
    database_url = f'sqlite:///{db_name}'

    # Create a SQLAlchemy engine. echo=True will log all SQL statements to stdout.
    engine = create_engine(database_url, echo=False)

    try:
        # Read the SQL schema from the file
        with open(schema_file, 'r') as f:
            schema_script = f.read()

        # Execute the schema script using a connection from the engine
        with engine.connect() as connection:
            # Split the schema script into individual statements and execute them
            # Filter out any empty strings that might result from splitting
            statements = [s.strip() for s in schema_script.split(';') if s.strip()]
            for statement in statements:
                connection.execute(text(statement))
            # Commit the transaction to save changes to the database
            connection.commit()
        print(f"Database '{db_name}' initialized successfully with schema from '{schema_file}'.")
    except FileNotFoundError:
        print(f"Error: Schema file '{schema_file}' not found.")
    except Exception as e:
        print(f"An error occurred during database preparation: {e}")

if __name__ == '__main__':
    # Set up argument parsing for command-line execution
    parser = argparse.ArgumentParser(description="Prepare a SQLite database from a SQL schema file.")
    parser.add_argument('db_name', help="The name of the SQLite database file (e.g., 'database.db').")
    parser.add_argument('schema_file', help="The path to the SQL schema file (e.g., 'schema.sql').")

    args = parser.parse_args()

    # Call the prepare_database function with arguments from the command line
    prepare_database(args.db_name, args.schema_file)