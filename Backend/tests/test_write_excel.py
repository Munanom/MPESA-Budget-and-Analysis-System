#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for ExelWriter class that writes iMessage data to an Excel file.
Uses pytest for testing.
"""

import pytest
from datetime import datetime
from os import scandir
from imessage_reader.write_excel import ExelWriter
from imessage_reader.data_container import MessageData


@pytest.fixture()
def create_directory(tmpdir):
    """
    Fixture to create a temporary directory for testing.

    :param tmpdir: pytest's fixture for creating temporary directories.
    :return: Path to the temporary directory.
    """
    directory = tmpdir.mkdir("sub/")
    yield directory


def message_data_one_row():
    """
    Provide a list of MessageData instances for testing.

    :return: A list containing a single MessageData instance with predefined values.
    """
    message_data_list = [
        MessageData(
            user_id="max.mustermann@icloud.com",
            text="Hello!",
            date="2020-10-27 17:19:20",
            service="SMS",
            account="+01 555 17172",
            is_from_me=1,
        )
    ]
    return message_data_list


def test_write_excel(create_directory):
    """
    Test the functionality of the ExelWriter class to write data to an Excel file.

    :param create_directory: Path to the temporary directory where the Excel file will be created.
    """
    excel_file_path = create_directory + "/sub"
    ew = ExelWriter(message_data_one_row(), excel_file_path)
    ew.write_data()

    file_name = ""
    dir_entries = scandir(create_directory)
    for entry in dir_entries:
        if entry.is_file():
            file_name = entry.name

    expected_file_name = (
        "sub" + f'iMessage-Data_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
    )

    assert len(create_directory.listdir()) == 1
    assert file_name == expected_file_name