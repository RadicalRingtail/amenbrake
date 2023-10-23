import os, venv, subprocess, platform

# automatically sets up a virual environment for development

current_dir = os.path.join(os.getcwd(), '.venv')

venv.create(current_dir, with_pip=True)

if platform.system() == 'Darwin':
    subprocess.run('.venv/bin/pip install -r requirements.txt', shell=True)
elif platform.system() == 'Windows':
    subprocess.run('.venv\Scripts\pip.exe install -r requirements.txt')