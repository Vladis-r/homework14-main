import sqlite3
from flask import jsonify

def search_by_title(title):
    """
    Функция для поиска фильма по его названию
    Сортировка по дате выхода
    Вывод в формате json
    """
    with sqlite3.connect("netflix.db") as connect:
        cursor = connect.cursor()
        sqlite_query =(f"""
        SELECT title, country, release_year, listed_in, description
        FROM netflix
        WHERE title LIKE '%{title}%'
        ORDER BY release_year DESC
        """)
        cursor.execute(sqlite_query)
        result = cursor.fetchall()

        output_by_title = []

        for r in result:
            output_by_title.append({
            "title": r[0],
            "country": r[1],
            "release_year": r[2],
            "genre": r[3],
            "description": r[4].rstrip('\n')
            })

        return jsonify(output_by_title)

def search_from_one_year_to_year(from_one_year, to_year):
    """
    Функция для поиска фильмов в промежутке между двумя годами включительно
    :param from_one_year: год с которого начать поиск
    :param to_year: год которым закончить поиск
    :return: Список фильмов в json
    """
    with sqlite3.connect("netflix.db") as connect:
        cursor = connect.cursor()
        sqlite_query =(f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {from_one_year} AND {to_year}
        LIMIT 100
        """)
        cursor.execute(sqlite_query)
        result = cursor.fetchall()

        output_by_years = []

        for r in result:
            output_by_years.append({
            "title": r[0],
            "release_year": r[1],
            })

        return jsonify(output_by_years)


def search_by_rating(rating):
    """
    Функция для поиска фильмов по рейтингу возрастных ограничений
    :param rating: рейтинг возрастных ограничений
    :return: список фильмов в json
    """
    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = (f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating IN {rating}
        """)
        cursor.execute(sqlite_query)
        result = cursor.fetchall()

        output_by_rating = []
        for r in result:
            output_by_rating.append({
            "title": r[0],
            "rating": r[1],
            "description": r[2].rstrip('\n')
            })

        return output_by_rating


def test_func(rating):
    with sqlite3.connect('../netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = (f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating IN {rating}
        """)
        cursor.execute(sqlite_query)
        result = cursor.fetchall()

        output_by_rating = []
        for r in result:
            output_by_rating.append({
            "title": r[0],
            "rating": r[1],
            "description": r[2].rstrip('\n')
            })
        for i in output_by_rating:
            print(i)
        print(output_by_rating)
        return jsonify(output_by_rating)

a = test_func("""('G')""")

