import subprocess
import sys
import os

os.chdir( os.path.abspath( os.path.dirname( __file__ ) ) )
sys.path.insert( 0 , "src" )

name = "langful"
version = __import__( name ).__version__

if len ( i := version.split( "." ) ) < 3 : version = ".".join( i + list( value for value in i.pop( -1 ) ) )

for count in range( 3 , 0 , -1 ) :
    try :
        print( f"{name} { version }\n" )
        assert ( commit := input( "commit\n> " ) )
        build = input( "\nbuild[Y/n](N)\n> " ).lower()
        build = True if build in [ "y" , "yes" ] else False
        if build :
            release = input( "\nrelease[Y/n](Y)\n> " ).lower()
            release = True if release in [ "n" , "no" ] else False
        else :
            release = False
        assert all( input( f"\nbe sure to update[Y/n](Y) ( update after { i - 1} )\n> " ).lower() not in [ "n" , "no" ] for i in range( 3 , 0 , -1 ) )
        input( f"\n{name} { version }\ncommit { commit }\nbuild { build }\nrelease { release }\n" )
    except ( KeyboardInterrupt , EOFError , AssertionError ) :
        print( f"input error try again (quit after { count - 1 } times)" )
    else :
        break
else :
    print( "exit" )
    exit()

subprocess.check_call( [ "git" , "add" , "." ] )
subprocess.check_call( [ "git" , "commit" , "-m" , commit ] )
subprocess.check_call( [ "git" , "push" , "origin" ] )
subprocess.check_call( [ sys.executable , "pack.py" ] ) if build else None
if release :
    subprocess.check_call( [ "git" , "tag" , version ] )
    subprocess.check_call( [ "git" , "push" , "origin" , "--tags" ] )
    subprocess.check_call( [ sys.executable , "-m" , "twine" , "upload" , "dist/*" ] )
