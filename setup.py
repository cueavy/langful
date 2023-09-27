import shutil
import pip
import sys
import os

pip.main( [ "install" , "--upgrade" , "setuptools" , "wheel" , "twine" , "pytest" ] )

import setuptools
import pytest

assert pytest.main( [ "./tests.py" , "-s" ] ) == 0 , "Test error"

name = "langful"
version = __import__( name ).__version__

def remove( path : str ) -> None :
    shutil.rmtree( path ) if os.path.exists( path ) else None

def clear() -> None :
    [ remove( path ) for path in [ os.path.join( f"{ name }" , "__pycache__" ) , f"{ name }.egg-info" , "build" ] ]

os.chdir( os.path.dirname( __file__ ) )
remove( "dist" )
clear()

upload = "-noask" not in sys.argv
sys.argv = [ "setup.py" , "bdist_wheel" ]

setuptools.setup(
    name = name ,
    version = version ,
    author = "cueavyqwp" ,
    author_email = "cueavyqwp@outlook.com" ,
    description = "provides internationalization for python" ,
    long_description = open( "README.md" , "r" , encoding = "utf-8" ).read() ,
    long_description_content_type = "text/markdown" ,
    url = "https://github.com/cueavy/langful" ,
    packages = setuptools.find_packages() ,
    classifiers = [
        "Programming Language :: Python :: 3" ,
        "License :: OSI Approved :: MIT License" ,
        "Operating System :: OS Independent" ,
    ] ,
    python_requires = '>= 3.9' ,
)

clear()

os.system( "twine upload dist/*" ) if upload and input( "pass enter to upload[Y/N]\n>" ).lower() in [ "y" , "yse" ] else ...
