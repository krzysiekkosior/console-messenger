from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'coderslab'
PORT = '5432'
DATABASE_NAME = 'workshop'

create_db_query = f"CREATE DATABASE {DATABASE_NAME};"
create_users_table_query = """
CREATE TABLE users(id serial, username varchar(255) UNIQUE, 
hashed_password varchar(80), PRIMARY KEY(id));
"""
create_messages_table_query = """
CREATE TABLE messages(id serial, from_id integer, to_id integer, text varchar(255), creation_date timestamp 
default CURRENT_TIMESTAMP, PRIMARY KEY(id), FOREIGN KEY(from_id) REFERENCES users(id) ON DELETE CASCADE, 
FOREIGN KEY(to_id) REFERENCES users(id) ON DELETE CASCADE);
"""

try:
    connection = connect(user=USER, password=PASSWORD, host=HOST, port=PORT)
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(create_db_query)
    except DuplicateDatabase as e:
        print(e)
    connection.close()
except OperationalError as e:
    print(e)

try:
    connection = connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DATABASE_NAME)
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(create_users_table_query)
    except DuplicateTable as e:
        print(e)
    try:
        cursor.execute(create_messages_table_query)
    except DuplicateTable as e:
        print(e)
    connection.close()
except OperationalError:
    print("Połączenie nieudane")
