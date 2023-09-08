import subprocess

subprocess.run('../../venv/Scripts/pyside6-designer.exe ./login_window.ui')
subprocess.run('../../venv/Scripts/pyside6-uic.exe ./login_window.ui -o ./login_window.py')