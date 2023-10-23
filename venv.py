import os, venv, subprocess

# automatically sets up a virual environment for development

current_dir = os.path.join(os.getcwd(), '.venv')

venv.create(current_dir, with_pip=True)
subprocess.run('.venv\Scripts\pip.exe install -r requirements.txt')