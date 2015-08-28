import pytest
from openjudge import cli


@pytest.fixture
def parser():
    p = cli.get_parser()
    return p


def test_get_parser():
    p = cli.get_parser()
    assert isinstance(p.description, str)
    assert len(p.description) != 0


def test_addition_of_arguments(parser):
    assert parser
    p = cli.add_arguments(parser)
    assert p
