#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module to create a SQLite3 database from iMessage data.
This module provides functionality to create a SQLite3 database containing iMessage data. The database is designed to store user-specific information including message text, date, and service details.
Classes:
    CreateDatabase: Manages the creation and population of the SQLite database.
Usage:
    Instantiate the `CreateDatabase` class with the necessary parameters and call the `create_sqlite_db` method to generate the database file.
Example:
    imessage_data = [
        MessageData(user_id="123", text="Hello", date="2024-09-18", service="iMessage", account="account1", is_from_me="1"),
        ...
    ]
    db_creator = CreateDatabase(imessage_data, "/path/to/directory/")
    db_creator.create_sqlite_db()
"""

import sqlite3


class CreateDatabase:
    """
    A class to create and manage an SQLite3 database from iMessage data.
    Attributes:
        imessage_data (list): A list of MessageData objects containing the iMessage details.
        file_path (str): The directory path where the SQLite database file will be saved.
    Methods:
        __init__(self, imessage_data: list, file_path: str):
            Initializes the CreateDatabase instance with iMessage data and file path.
        create_sqlite_db(self):
            Creates an SQLite3 database file and populates it with the iMessage data.
    """

    def __init__(self, imessage_data: list, file_path: str):
        """
        Initializes the CreateDatabase instance.
        :param imessage_data: List of MessageData objects with attributes: user_id, text, date, service, and account.
        :param file_path: Directory path where the SQLite database will be created.
        """
        self.imessage_data = imessage_data
        self.file_path = file_path

    def create_sqlite_db(self):
        """
        Creates a SQLite3 database and populates it with iMessage data.
        This method performs the following operations:
        - Creates a new SQLite3 database file at the specified location.
        - Creates a table named `Messages` with columns for user_id, message, date, service, destination_caller_id, and is_from_me.
        - Inserts the iMessage data into the `Messages` table.
        - Commits the transaction and closes the database connection.
        The database file will be saved in the specified directory with the name 'iMessage-Data.sqlite'.
        """
        database = self.file_path + "iMessage-Data.sqlite"

        conn = sqlite3.connect(database)
        cur = conn.cursor()

        # Drop the table if it exists
        cur.execute("DROP TABLE IF EXISTS Messages")

        # Create the Messages table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Messages (
                user_id TEXT,
                message TEXT,
                date TEXT,
                service TEXT,
                destination_caller_id TEXT,
                is_from_me TEXT
            )
            """
        )

        # Insert the iMessage data into the Messages table
        for data in self.imessage_data:
            cur.execute(
                """INSERT INTO Messages (user_id, message, date, service, destination_caller_id, is_from_me)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    data.user_id,
                    data.text,
                    data.date,
                    data.service,
                    data.account,
                    data.is_from_me,
                ),
            )

        conn.commit()
        cur.close()

        print()
        print(">>> SQLite database successfully created! <<<")
        print("You can find the Database at the specified path.")
        print()