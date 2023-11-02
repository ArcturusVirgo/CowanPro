import subprocess

subprocess.run('../../venv/Scripts/pyside6-designer.exe ./ReferenceLineWindow.ui')
subprocess.run('../../venv/Scripts/pyside6-uic.exe ./ReferenceLineWindow.ui -o ./ReferenceLineWindow.py')
