#!/usr/bin/env python3
"""
Tiny RESTful API in Python (Flask).

Changes from the original example:
  1. Added new book entries (ids 6 and 7) to the hard-coded JSON.
  2. Renamed every /books endpoint to /goodbooks.

Run on Mac (Terminal):
    python3 -m pip install flask
    python3 app.py
Or just double-click run_mac.command.

The app uses port 5001 because macOS uses port 5000 for AirPlay Receiver.
If 5001 is busy it picks the next free port and prints the address.
Your browser opens to the page automatically.
"""

import os
import socket
import threading
import webbrowser

from flask import Flask, jsonify, request, send_from_directory, abort

# Absolute path, so the app works no matter which folder Terminal is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))

# ---------------------------------------------------------------------------
# Hard-coded data (acts as our in-memory "database")
# ---------------------------------------------------------------------------
books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "rating": 5},
    {"id": 2, "title": "1984", "author": "George Orwell", "rating": 4},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "rating": 3},
    {"id": 4, "title": "Moby-Dick", "author": "Herman Melville", "rating": 2},
    {"id": 5, "title": "Pride and Prejudice", "author": "Jane Austen", "rating": 4},
    # NEW ENTRIES (requirement #1)
    {"id": 6, "title": "Mind Gym: An Athlete's Guide to Inner Excellence", "author": "Gary Mack & David Casstevens", "rating": 5},
    {"id": 7, "title": "The 48 Laws of Power", "author": "Robert Greene", "rating": 4},
]


def find_book(book_id):
    return next((b for b in books if b["id"] == book_id), None)


def validate_book(data, partial=False):
    """Return an error message, or None if the payload is valid."""
    if not isinstance(data, dict):
        return "Request body must be a JSON object."
    required = ["title", "author", "rating"]
    if not partial:
        missing = [f for f in required if f not in data]
        if missing:
            return f"Missing field(s): {', '.join(missing)}"
    if "rating" in data:
        r = data["rating"]
        if not isinstance(r, int) or isinstance(r, bool) or not 1 <= r <= 5:
            return "Rating must be a whole number from 1 to 5."
    for field in ("title", "author"):
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            return f"'{field}' must be a non-empty string."
    return None


# ---------------------------------------------------------------------------
# Front end
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ---------------------------------------------------------------------------
# REST endpoints — all renamed from /books to /goodbooks (requirement #2)
# ---------------------------------------------------------------------------
@app.route("/goodbooks", methods=["GET"])
def get_goodbooks():
    """READ all books -> 200 OK"""
    return jsonify(books), 200


@app.route("/goodbooks/<int:book_id>", methods=["GET"])
def get_goodbook(book_id):
    """READ one book -> 200 OK or 404 Not Found"""
    book = find_book(book_id)
    if book is None:
        abort(404, description=f"Book {book_id} not found.")
    return jsonify(book), 200


@app.route("/goodbooks", methods=["POST"])
def create_goodbook():
    """CREATE a book -> 201 Created or 400 Bad Request"""
    data = request.get_json(silent=True)
    error = validate_book(data)
    if error:
        abort(400, description=error)
    new_id = max((b["id"] for b in books), default=0) + 1
    book = {"id": new_id, "title": data["title"].strip(),
            "author": data["author"].strip(), "rating": data["rating"]}
    books.append(book)
    return jsonify(book), 201


@app.route("/goodbooks/<int:book_id>", methods=["PUT"])
def update_goodbook(book_id):
    """UPDATE a book -> 200 OK, 400 Bad Request, or 404 Not Found"""
    book = find_book(book_id)
    if book is None:
        abort(404, description=f"Book {book_id} not found.")
    data = request.get_json(silent=True)
    error = validate_book(data, partial=True)
    if error:
        abort(400, description=error)
    for field in ("title", "author", "rating"):
        if field in data:
            book[field] = data[field].strip() if isinstance(data[field], str) else data[field]
    return jsonify(book), 200


@app.route("/goodbooks/<int:book_id>", methods=["DELETE"])
def delete_goodbook(book_id):
    """DELETE a book -> 204 No Content or 404 Not Found"""
    book = find_book(book_id)
    if book is None:
        abort(404, description=f"Book {book_id} not found.")
    books.remove(book)
    return "", 204


# ---------------------------------------------------------------------------
# JSON error responses (instead of Flask's default HTML pages)
# ---------------------------------------------------------------------------
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def json_error(err):
    code = getattr(err, "code", 500)
    return jsonify({"error": getattr(err, "description", "Server error"), "status": code}), code


def find_free_port(start=5001, attempts=20):
    """Return the first free port at or after `start` (skips AirPlay's 5000)."""
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found between 5001 and 5020.")


if __name__ == "__main__":
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    print(f"\n  Good Books API running at {url}")
    print(f"  JSON endpoint:            {url}/goodbooks")
    print("  Press Ctrl + C to stop.\n")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    # use_reloader=False keeps one process, so the browser opens only once
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)
