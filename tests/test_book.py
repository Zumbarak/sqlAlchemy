from unittest.mock import patch, MagicMock
import pytest
from app.controllers.book import (
    create_book,
    list_books,
    update_book,
    delete_book,
    transfer_book,
)


# create_book
@patch("app.controllers.book.db")
@patch("app.controllers.book.Library")
@patch("app.controllers.book.Book")
def test_create_book_success(mock_book, mock_library, mock_db):
    mock_library.query.get.return_value = MagicMock()
    mock_book_instance = MagicMock()
    mock_book.return_value = mock_book_instance

    data = {"title": "Clean Code", "author": "Robert Martin", "library_id": 1}
    result = create_book(data)

    mock_book.assert_called_once()
    mock_db.session.add.assert_called_once_with(mock_book_instance)
    mock_db.session.commit.assert_called_once()
    assert result == mock_book_instance


def test_create_book_missing_fields():
    with pytest.raises(ValueError) as exc:
        create_book({"title": "Only title"})
    assert "Missing required fields" in str(exc.value)


@patch("app.controllers.book.db")
@patch("app.controllers.book.Library")
@patch("app.controllers.book.Book")
def test_create_book_library_not_found(mock_book, mock_library, mock_db):
    mock_library.query.get.return_value = None
    data = {"title": "Clean Code", "author": "Robert Martin", "library_id": 999}
    with pytest.raises(LookupError) as exc:
        create_book(data)
    assert "Library not found" in str(exc.value)


# list_books
@patch("app.controllers.book.db")
@patch("app.controllers.book.Book")
def test_list_books_no_filters(mock_book, mock_db):
    book1 = MagicMock(id=1, title="A", author="B", library_id=1, created_at=MagicMock())
    book2 = MagicMock(id=2, title="C", author="D", library_id=2, created_at=MagicMock())
    mock_book.query.all.return_value = [book1, book2]

    result = list_books()
    assert isinstance(result, list)
    assert len(result) == 2


@patch("app.controllers.book.db")
@patch("app.controllers.book.Book")
def test_list_books_with_library_id_filter(mock_book, mock_db):
    mock_query = MagicMock()
    mock_book.query.filter.return_value = mock_query
    mock_query.all.return_value = [MagicMock()]

    filters = {"library_id": 1}
    result = list_books(filters)

    mock_book.query.filter.assert_called_once_with(mock_book.library_id == 1)
    assert len(result) == 1


@patch("app.controllers.book.db")
@patch("app.controllers.book.Book")
def test_list_books_with_search_filter(mock_book, mock_db):
    mock_query = MagicMock()
    mock_book.query.filter.return_value = mock_query
    mock_query.all.return_value = [MagicMock()]

    filters = {"search": "Clean"}
    result = list_books(filters)

    assert mock_book.query.filter.called
    assert len(result) == 1


@patch("app.controllers.book.db")
@patch("app.controllers.book.Book")
def test_list_books_with_both_filters(mock_book, mock_db):
    mock_initial_query = MagicMock()
    mock_book.query = mock_initial_query

    mock_filter_result_1 = MagicMock()
    mock_initial_query.filter.return_value = mock_filter_result_1

    mock_filter_result_2 = MagicMock()
    mock_filter_result_1.filter.return_value = mock_filter_result_2

    mock_filter_result_2.all.return_value = [MagicMock()]

    filters = {"library_id": 1, "search": "Clean"}
    result = list_books(filters)

    mock_initial_query.filter.assert_called_once_with(mock_book.library_id == 1)
    mock_filter_result_1.filter.assert_called_once()
    assert len(result) == 1


# update_book
@patch("app.controllers.book.db")
@patch("app.controllers.book.Library")
def test_update_book_success(mock_library, mock_db):
    book_instance = MagicMock(library_id=1)
    mock_library.query.get.return_value = MagicMock()

    data = {"title": "Updated Title", "author": "New Author", "library_id": 2}
    result = update_book(book_instance, data)

    assert book_instance.title == "Updated Title"
    assert book_instance.author == "New Author"
    assert book_instance.library_id == 2
    mock_db.session.commit.assert_called_once()
    assert result == book_instance


@patch("app.controllers.book.db")
@patch("app.controllers.book.Library")
def test_update_book_library_not_found(mock_library, mock_db):
    book_instance = MagicMock(library_id=1)
    mock_library.query.get.return_value = None

    data = {"title": "Updated Title", "author": "New Author", "library_id": 999}
    with pytest.raises(LookupError) as exc:
        update_book(book_instance, data)
    assert "Library not found" in str(exc.value)


# delete_book
@patch("app.controllers.book.db")
def test_delete_book_success(mock_db):
    book_instance = MagicMock()
    delete_book(book_instance)
    mock_db.session.delete.assert_called_once_with(book_instance)
    mock_db.session.commit.assert_called_once()


# transfer_book
@patch("app.controllers.book.db")
@patch("app.controllers.book.Library")
def test_transfer_book_success(mock_library, mock_db):
    book_instance = MagicMock(library_id=1)
    new_library = MagicMock(id=2, name="New Library")
    mock_library.query.get_or_404.return_value = new_library

    data = {"new_library_id": 2}
    result = transfer_book(book_instance, data)
    assert book_instance.library_id == 2
    assert new_library == result


def test_transfer_book_missing_new_library():
    book_instance = MagicMock()
    with pytest.raises(ValueError) as exc:
        transfer_book(book_instance, {})
    assert "Missing new_library_id" in str(exc.value)


@patch("app.controllers.book.db")
@patch("app.controllers.book.Library")
def test_transfer_book_library_not_found(mock_library, mock_db):
    book_instance = MagicMock()
    mock_library.query.get_or_404.return_value = None  # Simulate library not found
    data = {"new_library_id": 999}
    with pytest.raises(LookupError) as exc:
        transfer_book(book_instance, data)
    assert "Library not found" in str(exc.value)
