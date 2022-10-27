from unittest.mock import MagicMock

import pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture
def test_input():
    g1 = Genre(id=1, name="comedy")
    g2 = Genre(id=2, name="horror")
    g3 = Genre(id=3, name="drama")

    return {
        1: g1,
        2: g2,
        3: g3
    }


@pytest.fixture
def genre_dao(test_input):
    genre_dao = GenreDAO(None)

    genre_dao.get_one = MagicMock(side_effect=test_input.get)
    genre_dao.get_all = MagicMock(return_value=test_input.values())
    genre_dao.create = MagicMock(return_value=Genre(id=4))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert len(genres) > 0

    def test_create(self):
        genre_d = {
            "name": "detective"
        }

        genre = self.genre_service.create(genre_d)

        assert genre.id is not None

    def test_delete(self):
        self.genre_service.delete(1)

    def test_update(self):
        genre_d = {
            "id": 1,
            "name": "detective"
        }

        self.genre_service.update(genre_d)
