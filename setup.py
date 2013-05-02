from distutils.core import setup
import py2exe

setup(
	windows=['gui.py'], 
	options = {
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"]
        }
    }
)
