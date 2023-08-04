import shutil
import pip
import sys
import os

name = "langful"
version = __import__( name ).__version__

pip.main( [ "install" , "--upgrade" , "setuptools" , "wheel" , "twine" ] )

import setuptools

def remove( path : str ) -> None :
    if os.path.exists( path ) :
        shutil.rmtree( path )

def clear() -> None :
    remove( os.path.join( f"{ name }" , "__pycache__" ) )
    remove( f"{ name }.egg-info" )
    remove( "build" )

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

if upload and input( "pass enter to upload[Y/N]\n>" ) in [ "y" , "Y" , "yse" , "Yes" ] :
    os.system( "twine upload dist/*" )
