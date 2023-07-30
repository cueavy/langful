from shutil import rmtree
import pip
import sys
import os

name = "langful"
version = "0.41"

pip.main( [ "install" , "--upgrade" , "setuptools" , "wheel" , "twine" ] )

import setuptools

if os.path.exists( "build" ) :
    rmtree( "build" )
if os.path.exists( f"{ name }.egg-info" ) :
    rmtree( f"{ name }.egg-info" )
if os.path.exists( "dist" ) :
    rmtree( "dist" )
if os.path.exists( os.path.join( f"{ name }" , "__pycache__" ) ) :
    rmtree( os.path.join( f"{ name }" , "__pycache__" ) )

upload = "-noask" not in sys.argv

sys.argv = [ "setup.py" , "bdist_wheel" ]

with open( "README.md" , "r" , encoding = "utf-8" ) as file :
    long_description = file.read()

setuptools.setup(
    name = name ,
    version = version ,
    author = "cueavyqwp" ,
    author_email = "cueavyqwp@outlook.com" ,
    description = "Help to localization" ,
    long_description = long_description ,
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

rmtree( "build" )
rmtree( f"{ name }.egg-info" )

if upload and input( "pass enter to upload\n>" ) in [ "y" , "Y" , "yse" , "Yes" ] :
    os.system( "twine upload dist/*" )
