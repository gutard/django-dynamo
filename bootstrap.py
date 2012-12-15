'''
This bootstrap script does the following:
a) Check if Pip is installed, and if not, installs Pip
b) Check if Virtualenv is installed, and if not, installs VirtualEnv via Pip
c) Create the virtualenv in Env and installs requirements into virtualenv
d) Creates a manage.bat / manage.sh script that links to the test project
'''

import os, sys, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__)) 
VIRTUAL_ENV_NAME='env'
VIRTUAL_ENV_DIR=os.path.join(ROOT,VIRTUAL_ENV_NAME)
REQUIREMENTS_FILE=os.path.join(ROOT,'requirements.txt')
DJANGO_MANAGE_FILE = os.path.join(ROOT,'tests','dynamo_project','manage.py')

OS_MANAGE_SCRIPT_WIN32='''@echo off
set CMD_LINE_ARGS=
:setArgs
if ""%%1""=="""" goto doneSetArgs
set CMD_LINE_ARGS=%%CMD_LINE_ARGS%% %%1
shift
goto setArgs
:doneSetArgs
"%s" "%s" %%CMD_LINE_ARGS%%
goto stop
:stop
'''

OS_MANAGE_SCRIPT_OSX='''%s "%s" "$@"'''



def bootstrap():
    try:
        import pip
    except ImportError:
        sys.stdout.write('Pip is not found and will be installed.\n')    
        subprocess.call(['sudo","easy_install","pip'])
        sys.stdout.write('Pip is now installed on your system.\n')
    else:
        sys.stdout.write('Pip is already installed on your system.\n')
    try:
        import virtualenv
    except ImportError:
        sys.stdout.write('Virtualenv is not found and will be installed using Pip.\n')
        subprocess.call(['pip", "install", "virtualenv'])        
        sys.stdout.write('Virtualenv is now installed on your system.\n')
    else:
        sys.stdout.write('Virtualenv is already installed on your system.\n')

def create_virtualenv():
    "Check if a virtual env existis, if not, create one"
    sys.stdout.write("Creation of Virtualenv starts.\n")    
    if 'VIRTUAL_ENV' not in os.environ:
        if not os.access(VIRTUAL_ENV_NAME,os.F_OK):
            sys.stdout.write('Virtualenv \"%s\" does not exist yet and will now be created.\n' %VIRTUAL_ENV_NAME)
            #subprocess.call(["virtualenv", VIRTUAL_ENV_NAME, "--no-site-packages"])
            subprocess.call(['virtualenv', VIRTUAL_ENV_NAME])  
            sys.stdout.write('Virtualenv \"%s\" is now created\n' %VIRTUAL_ENV_NAME)
        else:
            sys.stdout.write('Virtualenv \"%s\" already existed and will not be created.\n' %VIRTUAL_ENV_NAME)
    else:
         sys.stdout.write('Virtualenv \"%s\" already existed and will not be created.\n' %VIRTUAL_ENV_NAME)

def install_requirements():
    "Install the requirements into the virtualenv"
    sys.stdout.write("Installation of requirements into Virtualenv starts.\n")
    subprocess.call(["pip", "install", "-E", VIRTUAL_ENV_DIR, "--requirement",REQUIREMENTS_FILE])
    sys.stdout.write("Requirements are now installed/updated.\n")



def create_manage_command():
    sys.stdout.write("The manage command will now be created.\n") 
    if sys.platform =='win32':
        os_manage_filename='manage.bat'
        python_exe=os.path.join(VIRTUAL_ENV_DIR,'Scripts','python.exe')
        os_manage_script=OS_MANAGE_SCRIPT_WIN32
    else:
        os_manage_filename='manage.sh'
        python_exe=os.path.join(VIRTUAL_ENV_DIR,'bin','python')
        os_manage_script=OS_MANAGE_SCRIPT_OSX
    
    f = open(os_manage_filename,'w')
    f.write(os_manage_script %(python_exe,DJANGO_MANAGE_FILE))
    f.close()
    sys.stdout.write("The manage command has been created.\n")

if __name__ == '__main__':
    sys.stdout.write('***** Project Bootstrap starts. *****\n\n')

    bootstrap()
    sys.stdout.write('\n')
    create_virtualenv()
    sys.stdout.write('\n')
    install_requirements()
    sys.stdout.write('\n')
    create_manage_command()

    sys.stdout.write('\n***** Project Bootstrap is done.*****\n\n')
    sys.stdout.write('You can now run manage syncdb and manage runserver to have a test project up and running.\n\n')

    sys.exit(0)
