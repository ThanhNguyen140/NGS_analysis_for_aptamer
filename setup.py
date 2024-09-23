import sys
import os
from cx_Freeze import setup, Executable
# Add files

files = ["icon.ico","constants.py","control_panel/","GUI/","tools/","win/"]
python_dir = os.path.dirname(sys.executable)
targets = Executable(
    script = "AptaNext2.1.py",
    base = "Win32GUI",
    icon = "icon.ico"
)

# Setup CX_FREEZE
setup(name = "AptaNext2.1",
      version = "2.1.0",
      description = "Modified version of AptaNext",
      author="Phuong Thanh Nguyen",
      options = {"build.exe":{"include_files":files,'excludes':['tkinter','unittest']}},
      executables = [targets]
      )
