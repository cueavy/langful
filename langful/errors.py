"""
langful errors
"""

class LangfulError( Exception ) :

    def __init__( self , info : str = "" ) -> None :
        """
        langful errors
        """
        self.info = info

    def __str__( self ) -> str :
        return self.info

class DecodeError( LangfulError ) : ...
class LocaleError( LangfulError ) : ...
class ConfigError( LangfulError ) : ...
