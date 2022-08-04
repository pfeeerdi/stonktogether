import os
import time
import sqlalchemy

def connect_db():
    try:
        database_uri = str(os.getenv('SQLALCHEMY_DATABASE_URI')) + str(os.getenv('STANDARD_DATABASE'))
        engine = sqlalchemy.create_engine(database_uri)
        conn = engine.connect()
        conn.close()
    except:
        print("Retrying to connect ...")
        time.sleep(5)
        create_db()

def create_db():
    while (True):
        try:
            database_uri = str(os.getenv('SQLALCHEMY_DATABASE_URI')) + str(os.getenv('STANDARD_DATABASE'))
            new_database = str(os.getenv('DATABASE_NAME'))

            engine = sqlalchemy.create_engine(database_uri)
            conn = engine.connect()
            conn.execute("commit")
            conn.execute("create database " + new_database)
            conn.close()
            break
        except Exception as e:
            connect_db()
            break

def remove_db():
    print("Deleting ...")
    database_uri = str(os.getenv('SQLALCHEMY_DATABASE_URI')) + str(os.getenv('STANDARD_DATABASE'))
    new_database = str(os.getenv('DATABASE_NAME'))

    engine = sqlalchemy.create_engine(database_uri)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute(f"SELECT pg_terminate_backend (pid) FROM pg_stat_activity WHERE	pg_stat_activity.datname = '{new_database}';")
    conn.execute("drop database " + new_database)
    conn.close()
