"""
for mapping paths after building to exe
"""

import sys
import os


def get_file_name(filename):
    """watch to https://pythonhosted.org/PyInstaller/runtime-information.html#using-file-and-sys-meipass"""
    if sys._MEIPASS:
        filename = os.path.join(sys._MEIPASS, filename)
    return filename