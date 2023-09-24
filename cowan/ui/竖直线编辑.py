import subprocess

subprocess.run('../../venv/Scripts/pyside6-designer.exe ./reference_line_window.ui')
subprocess.run('../../venv/Scripts/pyside6-uic.exe ./reference_line_window.ui -o ./reference_line_window.py')

