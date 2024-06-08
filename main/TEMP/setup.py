from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt6'],
    'includes': ['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    'iconfile': '/Users/wanthinnn/Downloads/nekocoffee.icns'  # Đường dẫn đến file icon của ứng dụng (nếu có)
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
