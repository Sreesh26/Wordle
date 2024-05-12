from sqlalchemy import create_engine, Table, MetaData, Column, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'your_database_uri_here' with your actual database URI
DB_URI = 'postgresql://avnadmin:AVNS_PWrbvZPiqMp8rihRXrX@wordle-app-sriharsha07.a.aivencloud.com:13443/defaultdb?sslmode=require'
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Create MetaData instance
meta = MetaData()

# Reflect the existing database into the new MetaData instance
meta.reflect(bind=engine)

def add_column(engine, table_name, column):
    """
    Add a column to an existing table using raw SQL and the text object.
    """
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    
    # Format the SQL command
    sql = f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}'
    
    with engine.connect() as connection:
        # Use the text object to prepare the SQL command
        connection.execute(text(sql))
        # Commit the transaction
        connection.commit()

if __name__ == "__main__":
    # Check if the 'score' column exists to prevent re-adding it
    if 'score' not in meta.tables['users'].c:
        add_column(engine, 'users', Column('score', Integer, default=0))
        print("Column 'score' added to 'users' table.")
    else:
        print("Column 'score' already exists in 'users' table.")
