#!/usr/bin/env bash
set -e

BASE_URL="http://127.0.0.1:5000"
JSON="Content-Type: application/json"

echo "=============================="
echo " Libraries"
echo "=============================="

echo "Create library A"
curl -s -X POST "$BASE_URL/libraries" \
  -H "$JSON" \
  -d '{"name": "Central Library"}'
echo -e "\n"

echo "Create library B"
curl -s -X POST "$BASE_URL/libraries" \
  -H "$JSON" \
  -d '{"name": "Science Library"}'
echo -e "\n"

echo "List libraries"
curl -s "$BASE_URL/libraries"
echo -e "\n"


echo "=============================="
echo " Users"
echo "=============================="

echo "Create user Alice (library 1)"
curl -s -X POST "$BASE_URL/users" \
  -H "$JSON" \
  -d '{"name": "Alice", "library_id": 1}'
echo -e "\n"

echo "Create user Bob (library 2)"
curl -s -X POST "$BASE_URL/users" \
  -H "$JSON" \
  -d '{"name": "Bob", "library_id": 2}'
echo -e "\n"

echo "List users"
curl -s "$BASE_URL/users"
echo -e "\n"

echo "Get user 1"
curl -s "$BASE_URL/users/1"
echo -e "\n"


echo "=============================="
echo " Books"
echo "=============================="

echo "Create book 1 (library 1)"
curl -s -X POST "$BASE_URL/books" \
  -H "$JSON" \
  -d '{"title": "1984", "author": "George Orwell", "library_id": 1}'
echo -e "\n"

echo "Create book 2 (library 1)"
curl -s -X POST "$BASE_URL/books" \
  -H "$JSON" \
  -d '{"title": "Brave New World", "author": "Aldous Huxley", "library_id": 1}'
echo -e "\n"

echo "Create book 3 (library 2)"
curl -s -X POST "$BASE_URL/books" \
  -H "$JSON" \
  -d '{"title": "A Brief History of Time", "author": "Stephen Hawking", "library_id": 2}'
echo -e "\n"

echo "List all books"
curl -s "$BASE_URL/books"
echo -e "\n"

echo "List books in library 1"
curl -s "$BASE_URL/books?library_id=1"
echo -e "\n"

echo "Search books with '1984'"
curl -s "$BASE_URL/books?search=1984"
echo -e "\n"


echo "=============================="
echo " Book Updates"
echo "=============================="

echo "Update book 1 title"
curl -s -X PUT "$BASE_URL/books/1" \
  -H "$JSON" \
  -d '{"title": "Nineteen Eighty-Four"}'
echo -e "\n"

echo "Transfer book 1 to library 2"
curl -s -X POST "$BASE_URL/books/1/transfer" \
  -H "$JSON" \
  -d '{"new_library_id": 2}'
echo -e "\n"


echo "=============================="
echo " User Book Count"
echo "=============================="

echo "Get book count for user 1"
curl -s "$BASE_URL/users/1/books/count"
echo -e "\n"


echo "=============================="
echo " Deletes"
echo "=============================="

echo "Delete book 2"
curl -s -X DELETE "$BASE_URL/books/2"
echo -e "\n"

echo "Delete user 2"
curl -s -X DELETE "$BASE_URL/users/2"
echo -e "\n"

echo "Delete library 1"
curl -s -X DELETE "$BASE_URL/libraries/1"
echo -e "\n"

echo "=============================="
echo " Done"
echo "=============================="

