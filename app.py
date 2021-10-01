# Small library. Home work 13.1 Создание API

import json
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/<int:book_id>/')
def index(book_id):
    with open('books.json', encoding="utf-8") as f:
        books = json.load(f)
        for book in books:
            if book_id == book['id']:
                return render_template("one_book.html", book=book)
        return render_template("one_book.html", book={})



if __name__ == '__main__':
    app.run(debug=True)