from unittest.mock import patch, MagicMock
import pytest
from app.controllers.library import (
    create_library,
    list_libraries,
    update_library,
    delete_library,
)


# create_library
@patch("app.controllers.library.db")
@patch("app.controllers.library.Library")
def test_create_library_success(mock_library, mock_db):
    mock_library_instance = MagicMock()
    mock_library.return_value = mock_library_instance

    data = {"name": "Central Library"}

    result = create_library(data)

    mock_library.assert_called_once_with(name="Central Library")
    mock_db.session.add.assert_any_call(mock_library_instance)
    mock_db.session.commit.assert_called_once()
    assert result == mock_library_instance


def test_create_library_missing_name():
    with pytest.raises(ValueError) as exc:
        create_library({})
    assert "Missing required fields" in str(exc.value)


def test_create_library_no_data():
    with pytest.raises(ValueError) as exc:
        create_library(None)
    assert "Missing required fields" in str(exc.value)


# list_libraries
@patch("app.controllers.library.Library")
def test_list_libraries(mock_library):
    mock_library.query.all.return_value = [MagicMock(), MagicMock()]
    result = list_libraries()
    assert len(result) == 2


# update_library
@patch("app.controllers.library.db")
def test_update_library_success(mock_db):
    library_instance = MagicMock()
    data = {"name": "Updated Library"}

    result = update_library(library_instance, data)

    assert library_instance.name == "Updated Library"
    mock_db.session.commit.assert_called_once()
    assert result == library_instance


@patch("app.controllers.library.db")
def test_update_library_no_data(mock_db):
    library_instance = MagicMock()
    library_instance.name = "Original Name"
    result = update_library(library_instance, None)
    assert library_instance.name == "Original Name"
    mock_db.session.commit.assert_called_once()
    assert result == library_instance


@patch("app.controllers.library.db")
def test_update_library_empty_data(mock_db):
    library_instance = MagicMock()
    library_instance.name = "Original Name"
    result = update_library(library_instance, {})
    assert library_instance.name == "Original Name"
    mock_db.session.commit.assert_called_once()
    assert result == library_instance


# delete_library
@patch("app.controllers.library.db")
def test_delete_library_success(mock_db):
    library_instance = MagicMock()

    delete_library(library_instance)

    mock_db.session.delete.assert_called_once_with(library_instance)
    mock_db.session.commit.assert_called_once()
