from unittest.mock import patch, MagicMock
import pytest
from app.controllers.user import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    get_user_book_count,
)


# create_user
@patch("app.controllers.user.db")
@patch("app.controllers.user.Library")
@patch("app.controllers.user.User")
def test_create_user_success(mock_user, mock_library, mock_db):
    mock_user_instance = MagicMock()
    mock_user.return_value = mock_user_instance

    mock_library_instance = MagicMock()
    mock_library.return_value = mock_library_instance

    data = {"name": "Alice"}

    user, library = create_user(data)

    mock_user.assert_called_once_with(name="Alice")
    mock_library.assert_called_once_with(
        name="Alice's Library", user=mock_user_instance
    )
    mock_db.session.add.assert_any_call(mock_user_instance)
    mock_db.session.add.assert_any_call(mock_library_instance)
    mock_db.session.commit.assert_called_once()
    assert user == mock_user_instance
    assert library == mock_library_instance


def test_create_user_missing_name():
    with pytest.raises(ValueError) as exc:
        create_user({})
    assert "Missing name in request" in str(exc.value)


def test_create_user_no_data():
    with pytest.raises(ValueError) as exc:
        create_user(None)
    assert "Missing name in request" in str(exc.value)


# get_users
@patch("app.controllers.user.User")
def test_get_users(mock_user):
    mock_user.query.all.return_value = [MagicMock(), MagicMock()]
    result = get_users()
    assert len(result) == 2


@patch("app.controllers.user.User")
def test_get_user_success(mock_user):
    mock_user_instance = MagicMock()
    mock_user.query.get.return_value = mock_user_instance
    result = get_user(1)
    mock_user.query.get.assert_called_once_with(1)
    assert result == mock_user_instance


@patch("app.controllers.user.User")
def test_get_user_not_found(mock_user):
    mock_user.query.get.return_value = None
    with pytest.raises(LookupError) as exc:
        get_user(1)
    assert "User not found" in str(exc.value)


# update_user
@patch("app.controllers.user.db")
def test_update_user_success(mock_db):
    user_instance = MagicMock()
    data = {"name": "Bob"}

    result = update_user(user_instance, data)

    assert user_instance.name == "Bob"
    mock_db.session.commit.assert_called_once()
    assert result == user_instance


@patch("app.controllers.user.db")
def test_update_user_no_data(mock_db):
    with pytest.raises(ValueError) as exc:
        update_user(MagicMock(), None)
    assert "Missing name in request" in str(exc.value)


@patch("app.controllers.user.db")
def test_update_user_empty_data(mock_db):
    with pytest.raises(ValueError) as exc:
        update_user(MagicMock(), {})
    assert "Missing name in request" in str(exc.value)


# delete_user
@patch("app.controllers.user.db")
def test_delete_user_success(mock_db):
    user_instance = MagicMock()

    delete_user(user_instance)

    mock_db.session.delete.assert_called_once_with(user_instance)
    mock_db.session.commit.assert_called_once()


# get_user_book_count
@patch("app.controllers.user.Book")
def test_get_user_book_count_success(mock_book):
    library_instance = MagicMock()
    user_instance = MagicMock()
    user_instance.library = library_instance

    mock_query = mock_book.query.filter_by.return_value
    mock_query.count.return_value = 42

    result = get_user_book_count(user_instance)

    mock_book.query.filter_by.assert_called_once_with(library_id=library_instance.id)
    assert result == 42


def test_get_user_book_count_no_library():
    user_instance = MagicMock()
    user_instance.library = None

    with pytest.raises(LookupError) as exc:
        get_user_book_count(user_instance)
    assert "User does not have a library" in str(exc.value)
