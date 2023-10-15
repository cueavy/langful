import tkinter.ttk
import subprocess
import tkinter
import sys
import os

os.chdir( os.path.abspath( os.path.dirname( __file__ ) ) )
sys.path.insert( 0 , "src" )

name = "langful"
version = __import__( name ).__version__

if len ( i := version.split( "." ) ) < 3 : version = ".".join( i + list( value for value in i.pop( -1 ) ) )

class window :

    def __init__( self ) -> None :
        self.root = tkinter.Tk()
        self.root.title( "update" )
        self.root.geometry( "240x100" )

    def init( self ) -> None :
        ( frame := tkinter.Frame( self.root ) ).pack( fill = "both" , expand = True )

        tkinter.ttk.Checkbutton(frame).pack()

        tkinter.ttk.Separator( self.root ).pack( fill = "x" )
        tkinter.ttk.Button( self.root , text = "update" ).pack()

    def run( self ) -> None :
        self.init()
        self.root.mainloop()

    def update( self , commit : str , build : bool , release : bool ) -> None :
        subprocess.check_call( [ "git" , "add" , "." ] )
        subprocess.check_call( [ "git" , "commit" , "-m" , commit ] )
        subprocess.check_call( [ "git" , "push" , "origin" ] )
        subprocess.check_call( [ sys.executable , "pack.py" ] ) if build else None
        if release :
            subprocess.check_call( [ "git" , "tag" , version ] )
            subprocess.check_call( [ "git" , "push" , "origin" , "--tags" ] )
            subprocess.check_call( [ sys.executable , "-m" , "twine" , "upload" , "dist/*" ] )

if __name__ == "__main__" :
    root = window()
    root.run()
