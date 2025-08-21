from langful import func


def test() -> None:
    assert func.getlocale()
    assert func.getencoding()
