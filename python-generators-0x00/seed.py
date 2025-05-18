#!/usr/bin/env python3
"""
ALX Python Generators Project
Database Setup and Data Streaming with Generators
"""

import mysql.connector
from mysql.connector import Error
import uuid
import csv
from typing import Generator, Dict, Any

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Lonewolf92'  # Set your MySQL password here
}

def connect_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connected to MySQL Server")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise

def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")
        raise
    finally:
        cursor.close()

def connect_to_prodev() -> mysql.connector.connection.MySQLConnection:
    """Connect to the ALX_prodev database"""
    config = DB_CONFIG.copy()
    config['database'] = 'ALX_prodev'
    try:
        connection = mysql.connector.connect(**config)
        print("Connected to ALX_prodev database")
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        raise

def create_table(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create user_data table if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """)
        connection.commit()
        print("Table user_data created or already exists")
    except Error as e:
        print(f"Error creating table: {e}")
        raise
    finally:
        cursor.close()

def csv_data_generator(file_path: str) -> Generator[Dict[str, Any], None, None]:
    """Generator that yields rows from CSV file one by one"""
    with open(file_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            yield {
                'user_id': str(uuid.uuid4()),
                'name': row['name'],
                'email': row['email'],
                'age': float(row['age'])
            }

def insert_data(connection: mysql.connector.connection.MySQLConnection, data: Dict[str, Any]) -> None:
    """Insert data into the database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        # Check if email already exists
        cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (data['email'],))
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """, (data['user_id'], data['name'], data['email'], data['age']))
            connection.commit()
    except Error as e:
        print(f"Error inserting data: {e}")
        raise
    finally:
        cursor.close()

def main():
    """Main execution function"""
    try:
        # Step 1: Connect to MySQL server
        connection = connect_db()
        
        # Step 2: Create database
        create_database(connection)
        connection.close()
        
        # Step 3: Connect to ALX_prodev database
        prodev_conn = connect_to_prodev()
        
        # Step 4: Create table
        create_table(prodev_conn)
        
        # Step 5: Insert data from CSV using generator
        data_gen = csv_data_generator('user_data.csv')
        for data_row in data_gen:
            insert_data(prodev_conn, data_row)
            print(f"Inserted/Checked: {data_row['email']}")
        
        print("Database setup and data insertion complete!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'prodev_conn' in locals() and prodev_conn.is_connected():
            prodev_conn.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    main()