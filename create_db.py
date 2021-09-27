#!/usr/bin/python
import sqlite3


def connect_to_db():
    conn = sqlite3.connect('tasks_db')
    return conn


def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT,
                login TEXT,
                pass TEXT
            ); ''')

        conn.execute(''' 
             CREATE TABLE category (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL
            ); 
              ''')

        conn.execute('''
                    CREATE TABLE tasks
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        desc TEXT,
                        date_add DATE,
                        date_do DATE,
                        category_id INT,
                        user_id INT,
                        FOREIGN KEY (category_id) REFERENCES category (id) ON DELETE CASCADE ON UPDATE CASCADE,
                        CONSTRAINT tasks_users__fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
                    );

                ''')

        conn.commit()
        print("User table created successfully")
    except:
        print("User table creation failed - Maybe table")
    finally:
        conn.close()


create_db_table()
