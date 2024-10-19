import shutil
import os

class tmpdir :

    def __init__( self , path : str ) -> None :
        self.path = path

    def __enter__( self ) -> str :
        if os.path.exists( self.path ) : shutil.rmtree( self.path )
        os.mkdir( self.path )
        return self.path
    
    def __exit__( self , *_ ) -> None :
        shutil.rmtree( self.path )
