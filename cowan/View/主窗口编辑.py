import subprocess

subprocess.run('../../venv/Scripts/pyside6-designer.exe ./MainWindow.ui')
subprocess.run('../../venv/Scripts/pyside6-uic.exe ./MainWindow.ui -o ./MainWindowView.py')

