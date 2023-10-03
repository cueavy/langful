import subprocess
import shutil
import sys
import os

subprocess.check_call( [ sys.executable , "-m" , "pip" , "install" , "--upgrade" , "toml" , "twine" , "build" , "pytest" ] )

import toml
import pytest

os.chdir( os.path.dirname( __file__ ) )
upload = "-noask" not in sys.argv
sys.path.append( "src" )

assert pytest.main( [ "-s" ] ) == 0

with open( "pyproject.toml" , "r" , encoding = "utf-8" ) as file : data = toml.load( file )
data[ "project" ][ "version" ] = __import__( data[ "project" ][ "name" ] ).__version__
with open( "pyproject.toml" , "w" , encoding = "utf-8" ) as file : data = toml.dump( data , file )
shutil.rmtree( "dist" ) if os.path.exists( "dist" ) else None

subprocess.check_call( [ sys.executable , "-m" , "build" ] )

if upload :
    for _ in range( 3 ) :
        if input( "upload [Y/N]\n>" ) in [ "y" , "yes" ] : break
    else :
        quit()
    subprocess.check_call( [ sys.executable , "-m" , "twine" , "upload" , "dist/*" ] )
