import subprocess
import shutil
import sys
import os

subprocess.check_call( [ sys.executable , "-m" , "pip" , "install" , "--upgrade" , "toml" , "twine" , "build" , "pytest" ] )

import toml
import pytest

os.chdir( os.path.abspath( os.path.dirname( __file__ ) ) )
sys.path.insert( 0 , "src" )

assert pytest.main( [ "-s" ] ) == 0

data = {
    "project" : {
        "name" : ( name := "langful" ) ,
        "version" : __import__( name ).__version__ ,
        "description" : "provides internationalization for python" ,
        "readme" : "docs/README.md" ,
        "requires-python" : ">=3.10" ,
        "keywords" : [
            "i18n" ,
            "json" ,
            "internationalization"
        ] ,
        "classifiers" : [
            "Programming Language :: Python :: 3" ,
            "License :: OSI Approved :: MIT License" ,
            "Operating System :: OS Independent"
        ] ,
        "authors" : [
            {
                "name" : "cueavyqwp" ,
                "email" : "cueavy@outlook.com"
            }
        ] ,
        "license" : {
            "file" : "LICENSE"
        } ,
        "urls" : {
            "Homepage" : "https://github.com/cueavy/langful" ,
            "Source" : "https://github.com/cueavy/langful.git"
        }
    }
}

with open( "pyproject.toml" , "w" , encoding = "utf-8" ) as file : toml.dump( data , file )

shutil.rmtree( "dist" ) if os.path.exists( "dist" ) else None
subprocess.check_call( [ sys.executable , "-m" , "build" ] )
