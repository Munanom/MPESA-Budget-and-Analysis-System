#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for the CreateDatabase class.
Uses pytest for testing.
"""

import pytest
from os import scandir
from imessage_reader.create_sqlite import CreateDatabase
from imessage_reader.data_container import MessageData


@pytest.fixture()
def create_directory(tmpdir):
    """
    Fixture to create a temporary directory for testing.

    :param tmpdir: pytest's built-in fixture for temporary directories.
    :return: Path to the created temporary directory.
    """
    directory = tmpdir.mkdir("sub/")
    yield directory


def message_data_one_row():
    """
    Provides a sample MessageData list for testing.

    :return: List containing a single MessageData object.
    """
    message_data_list = [
        MessageData(
            user_id="max.mustermann@icloud.com",
            text="Hello Max!",
            date="2021-04-11 17:02:34",
            service="iMessage",
            account="+01 555 17172",
            is_from_me=1,
        )
    ]
    return message_data_list


def test_create_sqlite(create_directory):
    """
    Tests the creation of a SQLite database file.

    :param create_directory: Path to the temporary directory created by the fixture.
    """
    db_file_path = create_directory + "/db-"
    test_database = CreateDatabase(message_data_one_row(), db_file_path)
    test_database.create_sqlite_db()

    file_name = ""
    dir_entries = scandir(create_directory)
    for entry in dir_entries:
        if entry.is_file():
            file_name = entry.name

    expected_file_name = "db-" + "iMessage-Data.sqlite"

    assert len(create_directory.listdir()) == 1
    assert file_name == expected_file_name