# Small library. Home work 13.1 Создание API

import json
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/books/<int:book_id>/')
def index(book_id):
    with open('books.json', encoding="utf-8") as f:
        books = json.load(f)
        for book in books:
            if book_id == book['id']:
                # return render_template("one_book.html", book=book)
                return json.dumps(book, ensure_ascii=False)
        # return render_template("one_book.html", book={})
        return {}


@app.route('/add', methods=['POST'])
def add_book():
    new_book = request.json
    # return new_book
    return "", 201


@app.route('/add/')
def adding_book():
    return render_template("add_book.html")

if __name__ == '__main__':
    app.run(debug=True)