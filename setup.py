from cx_Freeze import setup, Executable
import sys
import os

os.environ['TCL_LIBRARY'] = 'C:\\Users\\delfina\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\Users\\delfina\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6'

buildOptions = dict(
    packages=[],
    excludes=[],
    include_files=['C:\\Users\\delfina\\AppData\\Local\\Programs\\Python\\Python36\\DLLs\\tcl86t.dll', 'C:\\Users\\delfina\\AppData\\Local\\Programs\\Python\\Python36\\DLLs\\tk86t.dll']
    
)


setup(
    name='ftdx1200_eq',
    description='blah',
    options=dict(build_exe=buildOptions),
executables=[Executable("ftdx1200_eq.py", base="Win32GUI", shortcutName="FTdx1200_EQ", shortcutDir="DesktopFolder")])