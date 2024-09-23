#!/usr/bin/env python3

"""
Data Container
Python 3.9+
"""

from dataclasses import dataclass

@dataclass
class MessageData:
    """Stores iMessage data: user ID, text, date, service, account, and sender status."""
    user_id: str
    text: str
    date: str
    service: str
    account: str
    is_from_me: int

    def __str__(self):
        """
        Returns a string representation of the MessageData object.

        :return: Formatted string containing all attributes.
        """
        return (
            f"user id:\t\t{self.user_id}\n"
            f"date and time:\t\t{self.date}\n"
            f"service:\t\t{self.service}\n"
            f"caller id:\t\t{self.account}\n"
            f"is_from_me:\t\t{self.is_from_me}\n"
            f"\n"
            f"text:\n"
            f"=====\n"
            f"{self.text}\n"
            f"\n"
            f"----------------------------------------------------------------\n"
        )