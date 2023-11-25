import subprocess

subprocess.run('../../venv/Scripts/pyside6-designer.exe ./DataShowWindow.ui')
subprocess.run('../../venv/Scripts/pyside6-uic.exe ./DataShowWindow.ui -o ./DataShowWindow.py')
