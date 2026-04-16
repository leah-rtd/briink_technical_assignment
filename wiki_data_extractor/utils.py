"""

This module provides utility functions for parsing and processing textual
data extracted from WikiRate responses.
"""


import re

def page_number_parser(comment: str) -> list:
    """
    Extract page number references from a comment string.

    The function searches for patterns such as "p. 12" or "P. 34"
    and returns all matches.

    Args:
        comment (str): A text string containing comments or references.

    Returns:
        list[str]: A list of detected page references.

    Example:
        >>> page_number_parser("See details on p. 12 and P. 45.")
        ['p. 12', 'P. 45']
    """

    pattern = r'\b[Pp]\.\s*\d+\b'
    matches = re.findall(pattern, comment)

    return matches
