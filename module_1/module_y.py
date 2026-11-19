"""
Formatting and reporting utilities for the parallel agent-session example.

This module is intentionally correct but lightly documented. It is designed for
the "Session B" agent task: improve docstrings in this file and update README.md,
without modifying any test files.
"""

from __future__ import annotations


def format_currency(amount: float) -> str:
    """Format a number as a US-dollar string with thousands separators.

    Negative amounts get a leading minus sign before the dollar sign.

    Args:
        amount: The value to format.

    Returns:
        The amount rounded to two decimal places, e.g. ``"$1,234.50"`` or
        ``"-$12.00"``.
    """
    if amount < 0:
        return f"-${abs(amount):,.2f}"
    return f"${amount:,.2f}"


def build_report_title(project_name: str, version: str) -> str:
    """Build a report title in the form ``"<project> — <version>"``.

    Whitespace in the project name is collapsed to single spaces, and both
    values are stripped. Blank inputs fall back to defaults.

    Args:
        project_name: Project name. Defaults to ``"Untitled Project"`` if blank.
        version: Version label. Defaults to ``"draft"`` if blank.

    Returns:
        The title, joined with an em dash, e.g. ``"Acme App — 1.2.0"``.
    """
    clean_project = " ".join(project_name.strip().split())
    clean_version = version.strip()

    if not clean_project:
        clean_project = "Untitled Project"
    if not clean_version:
        clean_version = "draft"

    return f"{clean_project} — {clean_version}"


def mask_email(email: str) -> str:
    """Mask the local part of an email address for safe display.

    The first and last characters of the local part are kept and the rest are
    replaced with ``*``. A one-character local part becomes ``"*"`` and a
    two-character one keeps only its first character. The domain is lowercased.

    Args:
        email: The address to mask. Surrounding whitespace is ignored.

    Returns:
        The masked address, e.g. ``"j**n@example.com"`` for ``"john@Example.com"``.

    Raises:
        ValueError: If ``email`` has no ``@``, or the local part or domain is
            empty.
    """
    email = email.strip()
    if "@" not in email:
        raise ValueError("email must contain @")

    local_part, domain = email.split("@", 1)
    if not local_part or not domain:
        raise ValueError("email must include a local part and domain")

    if len(local_part) == 1:
        masked_local = "*"
    elif len(local_part) == 2:
        masked_local = local_part[0] + "*"
    else:
        masked_local = local_part[0] + "*" * (len(local_part) - 2) + local_part[-1]

    return f"{masked_local}@{domain.lower()}"


def generate_summary_line(name: str, status: str, score: int) -> str:
    """Build a one-line summary in the form ``"<Name>: <status> (<score>)"``.

    The name has its whitespace collapsed and is title-cased; a blank name
    becomes ``"Unknown"``. The status is stripped, lowercased, and has
    underscores replaced with spaces.

    Args:
        name: Display name of the subject.
        status: Status label, e.g. ``"IN_PROGRESS"``.
        score: Numeric score shown in parentheses.

    Returns:
        The summary line, e.g. ``"Ada Lovelace: in progress (92)"``.
    """
    display_name = " ".join(name.strip().split()).title()
    display_status = status.strip().lower().replace("_", " ")

    if not display_name:
        display_name = "Unknown"

    return f"{display_name}: {display_status} ({score})"


def create_markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    """Render rows of data as a Markdown table.

    Columns appear in the order given. Each cell is converted with ``str()``;
    a key missing from a row produces an empty cell, and keys not listed in
    ``columns`` are ignored. Values are not escaped, so a ``|`` in a value will
    break the table layout.

    Args:
        rows: One dict per table row, mapping column name to value.
        columns: Column names to use as the header, in display order.

    Returns:
        The table as newline-separated lines: header, separator, then one line
        per row. With no rows, only the header and separator are returned.

    Raises:
        ValueError: If ``columns`` is empty.
    """
    if not columns:
        raise ValueError("columns cannot be empty")

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"

    body_lines = []
    for row in rows:
        values = [str(row.get(column, "")) for column in columns]
        body_lines.append("| " + " | ".join(values) + " |")

    return "\n".join([header, separator, *body_lines])


def truncate_text(text: str, max_length: int = 80) -> str:
    """Collapse whitespace in ``text`` and shorten it to ``max_length`` characters.

    If the cleaned text is longer than ``max_length``, it is cut and ``"..."``
    is appended so the result is at most ``max_length`` characters long.
    Trailing whitespace before the ellipsis is removed.

    Args:
        text: The text to shorten. Runs of whitespace become single spaces.
        max_length: Maximum length of the result, including the ellipsis.
            Defaults to 80.

    Returns:
        The cleaned text, unchanged if it fits, otherwise truncated with
        ``"..."``.

    Raises:
        ValueError: If ``max_length`` is less than 4.
    """
    if max_length < 4:
        raise ValueError("max_length must be at least 4")

    clean_text = " ".join(text.strip().split())
    if len(clean_text) <= max_length:
        return clean_text

    return clean_text[: max_length - 3].rstrip() + "..."
