from langful import locale

def test() -> None :
    assert locale.getlocale()
    assert locale.getencoding()
