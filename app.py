# Small library. Home work 13.1 Создание API

import json
from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route('/books/<int:book_id>/')
def index(book_id):
    with open('books.json', encoding="utf-8") as f:
        books = json.load(f)
        body = json.dumps({"error": "book not found"})
        status = '400'
        for book in books:
            if book_id == book['id']:
                body = json.dumps(book, ensure_ascii=False)
                status = '200'

        response = Response(body, content_type='application/json', status=status)
        return response


@app.route('/add', methods=['POST'])
def add_book():
    new_book = request.json
    # new_book['id'] = 2
    # new_book['isbn'] = "978-5-389-07435-5"

    return json.dumps(new_book), 201


@app.route('/add/')
def adding_book():
    return render_template("add_book.html")

if __name__ == '__main__':
    app.run(debug=True)