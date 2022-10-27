from unittest.mock import MagicMock

import pytest

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture
def test_input():
    d1 = Director(id=1, name="Lena")
    d2 = Director(id=2, name="Sveta")
    d3 = Director(id=3, name="Misha")

    return {
        1: d1,
        2: d2,
        3: d3
    }


@pytest.fixture
def director_dao(test_input):
    director_dao = DirectorDAO(None)

    director_dao.get_one = MagicMock(side_effect=test_input.get)
    director_dao.get_all = MagicMock(return_value=test_input.values())
    director_dao.create = MagicMock(return_value=Director(id=4))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) > 0

    def test_create(self):
        director_d = {
            "name": "Oleg"
        }

        director = self.director_service.create(director_d)

        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_d = {
            "id": 1,
            "name": "Gena"
        }

        self.director_service.update(director_d)
