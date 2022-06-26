import sqlite3
from collections import Counter
import json
from flask import jsonify
from pprint import pprint as pp

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

def search_by_rating(age_rating):
    """
    Функция для поиска фильмов по рейтингу возрастных ограничений
    :param rating: рейтинг возрастных ограничений
    :return: список фильмов в json
    """
    rating_parameters = {
        "children": ('G', ''),
        "family": ('G', 'PG', 'PG-13'),
        "adult": ('R', 'NC-17')
    }

    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = (f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating IN {rating_parameters[age_rating]}
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

        return jsonify(output_by_rating)


def search_by_genre(genre):
    """
    Функция для поиска фильмов по жанру
    :param genre: жанр фильма
    :return: список 10 самых свежих фильмов
    """
    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = (f"""
        SELECT title, description, release_year
        FROM netflix
        WHERE listed_in LIKE '%{genre}%'
        ORDER BY release_year DESC
        LIMIT 10
        """)
        cursor.execute(sqlite_query)
        result = cursor.fetchall()

        output_by_genre = []
        for r in result:
            output_by_genre.append({
            "title": r[0],
            "description": r[1].rstrip('\n')
            })

        return jsonify(output_by_genre)

def search_by_actors(actor1, actor2):
    with sqlite3.connect('../netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = (f"""
        SELECT "cast"
        FROM netflix
        WHERE "cast" LIKE '%{actor1}%' AND "cast" LIKE '%{actor2}%'
        """)
        cursor.execute(sqlite_query)
        result = cursor.fetchall()

        list_of_actors = []

        for res in result:
            list_of_actors.extend(res[0].split(', '))

        counter = Counter(list_of_actors)
        result_list = []
        for actor, count in counter.items():
            if actor not in [actor1, actor2] and count > 2:
                result_list.append(actor)

        return result_list

def search_by_request(type, year, genre):
    with sqlite3.connect('../netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = (f"""
           SELECT title, description
           FROM netflix
           WHERE type = '{type}' AND release_year = {year} AND listed_in LIKE '%{genre}%'
           """)
        cursor.execute(sqlite_query)
        result = cursor.fetchall()
        output_by_request = []
        for r in result:
            output_by_request.append({
            "title": r[0],
            "description": r[1].rstrip('\n')
            })

        return pp(json.dumps(output_by_request))
