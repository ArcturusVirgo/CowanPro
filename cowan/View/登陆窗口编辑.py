import subprocess

subprocess.run('../../venv/Scripts/pyside6-designer.exe ./LoginWindow.ui')
subprocess.run('../../venv/Scripts/pyside6-uic.exe ./LoginWindow.ui -o ./LoginWindowView.py')
