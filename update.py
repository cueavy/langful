import tkinter.messagebox
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
        self.root.resizable( False , False )

    def init( self ) -> None :
        ( frame := tkinter.Frame( self.root ) ).pack( fill = "both" , expand = True )
        self.entry = tkinter.ttk.Entry( frame )
        self.entry.pack( fill = "x" )
        tkinter.Label( f := tkinter.Frame( frame ) , text = "release" ).pack( side = "left" , fill = "x" )
        checkbutton = tkinter.ttk.Checkbutton( f , variable = ( i := tkinter.BooleanVar() ) )
        checkbutton.pack( side = "right" , fill = "x" )
        self.checkbutton = i
        f.pack( expand = True )
        tkinter.ttk.Separator( self.root ).pack( fill = "x" )
        tkinter.ttk.Button( self.root , text = "update" , command = self.update ).pack()

    def run( self ) -> None :
        self.init()
        self.root.mainloop()

    def update( self ) -> None :
        try :
            assert ( commit := self.entry.get() ) , "no commint"
            assert all( tkinter.messagebox.askokcancel( "update" , f"are you sure to update ( update after { _ } times )" ) for _ in range( 10 , 0 , -1 ) ) , "user cancel"
        except AssertionError as e :
            tkinter.messagebox.showwarning( "cancel" , str( e ) )
            return
        subprocess.check_call( [ "git" , "add" , "." ] )
        subprocess.check_call( [ "git" , "commit" , "-m" , commit ] )
        subprocess.check_call( [ "git" , "push" , "origin" ] )
        if self.checkbutton.get() :
            subprocess.check_call( [ sys.executable , "pack.py" ] )
            subprocess.check_call( [ "git" , "tag" , version ] )
            subprocess.check_call( [ "git" , "push" , "origin" , "--tags" ] )
            subprocess.check_call( [ sys.executable , "-m" , "twine" , "upload" , "dist/*" ] )
        self.root.destroy()

if __name__ == "__main__" :
    root = window()
    root.run()
