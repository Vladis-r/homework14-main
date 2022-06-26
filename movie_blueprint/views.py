from flask import Blueprint

from movie_blueprint.utils import search_by_title, search_from_one_year_to_year, search_by_rating

movie_blueprint = Blueprint('movie_blueprint', __name__)


@movie_blueprint.route('/movie/<title>')
def search_movies_by_title(title):
    return search_by_title(title)


@movie_blueprint.route('/movie/<from_one_year>/to/<to_year>')
def search_movies_by_years(from_one_year, to_year):
    return search_from_one_year_to_year(from_one_year, to_year)


@movie_blueprint.route('/rating/<age_rating>')
def search_by_rating(age_rating):
    if age_rating == "children":
        # rating = """('G')"""
        return search_by_rating("""('G')""")
