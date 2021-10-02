# Small library. Home work 13.1 Создание API

import json
from flask import Flask, render_template, request, Response

app = Flask(__name__)


def get_next_id(source_list, source_field):
    next_id = 1
    for item in source_list:
        if item[source_field] > next_id:
            next_id = item[source_field]
    next_id += 1
    return next_id

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

@app.route('/add/', methods=['POST'])
def add_book():
    if request.get_json():
        new_book = request.get_json()
        with open('books.json', encoding="utf-8") as f:
            books = json.load(f)
        new_book['id'] = get_next_id(books, "id")
        new_book['isbn'] = "978-5-389-07435-5"

        books.append(new_book)
        with open("books.json", "w", encoding="utf-8") as write_file:
            json.dump(books, write_file, ensure_ascii=False)

        return "Успешно добавлено", 201
    return "Ошибка передачи данных в виде JSON", 400
# Execute in terminal for test POST
# curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Fantastic\",\"author\":\"Popp\"}" http://127.0.0.1:5000/add/ --verbos


if __name__ == '__main__':
    app.run(debug=True)