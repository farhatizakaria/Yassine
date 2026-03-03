"""
Bootstrap script for LUS RSIS Management System.

This helper can be executed with the system Python interpreter and will:

* create a virtual environment in ``venv`` if it doesn't already exist
* install ``requirements.txt`` into that environment
* print a short reminder showing how to activate the environment and start
  the server

The goal is to make the project runnable with a single cross-platform command
(``python bootstrap.py``) on Linux, macOS and Windows.

Usage::

    python bootstrap.py

"""
import os
import sys
import subprocess

VENV_DIR = 'venv'
REQUIREMENTS = 'requirements.txt'


def create_venv():
    if not os.path.isdir(VENV_DIR):
        print(f"creating virtual environment in {VENV_DIR}...")
        subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])
    else:
        print(f"virtual environment {VENV_DIR} already exists; skipping creation")


def install_requirements():
    pip_path = os.path.join(
        VENV_DIR,
        'Scripts' if os.name == 'nt' else 'bin',
        'pip',
    )
    print('installing dependencies...')
    subprocess.check_call([pip_path, 'install', '-r', REQUIREMENTS])


def usage_message():
    activate_cmd = (
        f"{VENV_DIR}\\Scripts\\activate" if os.name == 'nt' else f"source {VENV_DIR}/bin/activate"
    )
    print('\nSetup complete. To run the application:')
    print(f'    {activate_cmd}    # activate the virtual environment')
    print('    python run.py  # start the server')


if __name__ == '__main__':
    try:
        create_venv()
        install_requirements()
        usage_message()
    except subprocess.CalledProcessError as exc:
        print('A command failed:', exc)
        sys.exit(1)
