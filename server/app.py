import psycopg2
import json
import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)

writers = [
    (1, 'Достоевский, Ф.М.'),
    (2, 'Булгаков, М.А.'),
    (3, 'Куприн, А.И.')
]

books = [
    (2, 'Собачье сердце'),
    (1, 'Преступление и наказание'),
    (1, 'Игрок'),
    (3, 'Гранатовый браслет'),
    (3, 'Поединок'),
    (2, 'Мастер и Маргарита'),
    (1, 'Братья Карамазовы'),
    (1, 'Идиот')
]

url = os.environ.get("DATABASE_URL") 
connection = psycopg2.connect(url)

@app.post("/init")
def db_init():
    cursor = connection.cursor()
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS writers, books')
            cursor.execute('CREATE TABLE writers (id serial PRIMARY KEY, name varchar (50) NOT NULL)')
            values = ', '.join([str(writer) for writer in writers])
            cursor.execute('INSERT INTO writers (id, name) VALUES ' + values)
            cursor.execute('CREATE TABLE books (id serial PRIMARY KEY, author_id INT, title varchar (100) NOT NULL)')
            values = ', '.join([str(book) for book in books])
            cursor.execute('INSERT INTO books (author_id, title) VALUES ' + values)
     
    return 'Tables \'writers\' and \'books\' has been initialized.', 201

@app.get("/show")
def show_writers():
    cursor = connection.cursor()
    cursor.execute('SELECT json_agg(writers) FROM writers')
    row = cursor.fetchone()
	
    if row[0] is not None:
        row = row[0]
    
    cursor.close()
    return json.dumps(row, ensure_ascii=False, indent=4)

@app.get("/writers/<int:writer_id>")
def get_books(writer_id):
    cursor = connection.cursor()
    cursor.execute('''SELECT json_agg(writers) FROM (SELECT writers.id, name, jsonb_agg(to_jsonb(books) - \'author_id\') AS books FROM writers 
        LEFT JOIN books ON (writers.id = books.author_id) GROUP BY writers.id HAVING writers.id = %s) AS writers''', str(writer_id))
    row = cursor.fetchone()
	
    if row[0] is not None:
        row = row[0][0]
    
    cursor.close()
    return json.dumps(row, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    app.run()
