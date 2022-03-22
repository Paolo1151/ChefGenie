import subprocess
import sys
import os
import platform

def install(package=None, requirements_install=False):
    if not requirements_install and not package:
        raise Exception("Please Put Package!")

    if requirements_install:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    else:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def install_packages():
    if platform.system() == 'Windows':
        os.system(".\\devenv\\Scripts\\activate && pip install -r requirements.txt && python3 -m spacy download en_core_web_md")
    else:
        os.system("source devenv/bin/activate && pip install -r requirements.txt && python3 -m spacy download en_core_web_md")

def call_module(module, *args):
    subprocess.check_call([sys.executable, '-m', module] + list(args))

def print_message(message):
    print('-'*20)
    print(message)
    print('-'*20)

def main():
    os.system('cls')
    os.system('python3 -m pip install --upgrade pip')
    print_message("Starting Creation of Dev Virtual Env!")
    install('virtualenv')
    call_module('virtualenv', 'devenv')
    install_packages()
    print_message("Creation Done!")
    


if __name__ == '__main__':
    main()