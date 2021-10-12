# Small library. Home work 13.1 Создание API

import json
from flask import Flask, render_template, request, Response

app = Flask(__name__)


def read_json():
    with open('books.json', encoding="utf-8") as f:
        books = json.load(f)
        return books


def save_json(books):
    with open("books.json", "w", encoding="utf-8") as write_file:
        json.dump(books, write_file, ensure_ascii=False)


def get_next_id(source_list, source_field):
    next_id = 1
    if source_list:
        for item in source_list:
            if item[source_field] > next_id:
                next_id = item[source_field]
        next_id += 1
    return next_id


def get_next_isbn(source_list, source_field): # Определяем следующий номер isbn
    """Перебираем все существующие номера.
    Преобразуем в число и находим максимальный.
    Прибавляем единицу, учитывая условия.
    Преобразуем в номер типа 978-5-389-07435-4
    """
    next_isbn_int = 1
    for item in source_list: # Находим максимальный номер isbn
        current_isbn = item[source_field]
        current_isbn = current_isbn.replace("-", "") # переводим в число
        if int(current_isbn) > next_isbn_int:
            next_isbn_int = int(current_isbn)
    next_isbn_int += 1 # Следующий номер в виде числа
    str_isbn = (str(next_isbn_int)).zfill(13) # Заполняем нулями слева, если длина номера меньше 13 символов
    isbn = [0, 0, 0, 0, 0]
    isbn[0] = int(str_isbn[0:3]) # Разбиваем по секциям
    isbn[1] = int(str_isbn[3])
    isbn[2] = int(str_isbn[4:7])
    isbn[3] = int(str_isbn[7:12])
    isbn[4] = int(str_isbn[12])
    # Применяем условия для isbn
    if isbn[4] > 4:
        isbn[4] = 0
        isbn[3] += 1
    if isbn[3] > 9999:
        isbn[3] = 0
        isbn[2] += 1
    if isbn[2] > 999:
        isbn[2] = 0
        isbn[1] += 1
    if isbn[1] > 6:
        isbn[1] = 0
        isbn[0] += 1
    # форматируем по шаблону 978-5-389-07435-4
    next_isbn = ('{:03d}-{}-{:03d}-{:05d}-{}'.format(isbn[0], isbn[1], isbn[2], isbn[3], isbn[4]))
    return next_isbn


@app.route('/books/<int:book_id>/')
def index(book_id):
    books = read_json()
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
        books = read_json()
        new_book['id'] = get_next_id(books, "id")
        new_book['isbn'] = get_next_isbn(books, "isbn")

        books.append(new_book)
        save_json(books) # Save to file

        return "Успешно добавлено", 201
    return "Ошибка передачи данных в виде JSON", 400
# Execute in terminal for test POST
# curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Fantastic\",\"author\":\"Popp\"}" http://127.0.0.1:5000/add/ --verbos


if __name__ == '__main__':
    app.run(debug=True)