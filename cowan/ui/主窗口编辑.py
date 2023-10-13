import subprocess

subprocess.run('../../venv/Scripts/pyside6-designer.exe ./main_window.ui')
subprocess.run('../../venv/Scripts/pyside6-uic.exe ./main_window.ui -o ./main_window.py')

