from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.model.genre import Genre
from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture
def test_input():
    genre = Genre(id=1)
    director = Director(id=1)
    m1 = Movie(id=1, title="Title1", genre=genre, director=director)
    m2 = Movie(id=2, title="Title2", genre=genre, director=director)
    m3 = Movie(id=3, title="TITLE3", genre=genre, director=director)

    return {
        1: m1,
        2: m2,
        3: m3
    }


@pytest.fixture
def movie_dao(test_input):
    movie_dao = MovieDAO(None)

    movie_dao.get_one = MagicMock(side_effect=test_input.get)
    movie_dao.get_all = MagicMock(return_value=test_input.values())
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "title": "Rive"
        }

        movie = self.movie_service.create(movie_d)

        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "id": 1,
            "title": "Name"
        }

        self.movie_service.update(movie_d)

    def test_partially_update(self):
        movie_d = {
            "id": 1,
            "title": "Name"
        }

        self.movie_service.partially_update(movie_d)
