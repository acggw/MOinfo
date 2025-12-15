import pytest
from unittest.mock import MagicMock
from database.tables.government import Government, print_governments

# -------------------------------
# 1️ Test Government object creation
# -------------------------------
def test_government_instantiation():
    govt = Government(name="Missouri", under="USA")

    assert govt.name == "Missouri"
    assert govt.under == "USA"

# -------------------------------
# 2️ Test print_governments prints correctly
# -------------------------------
def test_print_governments(capsys):
    mock_session = MagicMock()
    govt1 = Government(name="USA", under="USA")
    govt2 = Government(name="Missouri", under="USA")

    # Mock query
    mock_session.query.return_value.all.return_value = [govt1, govt2]

    print_governments(mock_session)

    captured = capsys.readouterr()
    assert "Printing Governments" in captured.out
    assert "USA -> USA" in captured.out
    assert "Missouri -> USA" in captured.out
