from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
from pathlib import Path  # Import Path for file path handling
import sqlite3  # Import sqlite3 for SQLite database handling

def create_db(db_uri: str,mysql_host=None, mysql_user=None, mysql_db=None) -> SQLDatabase:
    """
    Creates and returns an SQLDatabase instance based on the provided database URI.

    Args:
        db_uri (str): The database URI. Supported types are sqlite and mysql.

    Returns:
        SQLDatabase: An instance of SQLDatabase connected to the specified database.
    """
    try:
        if db_uri=="USE_LOCALDB":
            dbfilepath=(Path(__file__).parent/"STUDENT.db").absolute()
            print(f"Database file path: {dbfilepath}")
            creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
            # Use the creator function for SQLite
            engine = create_engine("sqlite:///", creator=creator)
        elif db_uri=="USE_MYSQLDB":
            if not all([mysql_host, mysql_user, mysql_db]):
                raise ValueError("MySQL connection details are incomplete.")
            # Create MySQL connection string
            connection_string = f"mysql+pymysql://{mysql_user}@{mysql_host}/{mysql_db}"
            print(connection_string)
            engine = create_engine(connection_string)
        
        # Create and return SQLDatabase instance
        return SQLDatabase(engine)
    except Exception as e:
        raise ValueError(f"Failed to create database connection: {e}")