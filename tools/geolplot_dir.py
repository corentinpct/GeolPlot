import os

def make_directories(directory,state):
    for locality in state['Locality'].keys():
        if not os.path.exists(f'{directory}/{locality}'):
            os.makedirs(f'{directory}/{locality}')
        for unit in state['Unit'].keys():
            if not os.path.exists(f'{directory}/{locality}/{unit}'):
                os.makedirs(f'{directory}/{locality}/{unit}')

def open_directory(directory):
    os.system(f'explorer "{os.path.abspath(directory)}"') if os.name == 'nt' else os.system(f'xdg-open "{os.path.abspath(directory)}"')

def get_directory(directory,locality,unit):
    return f'{directory}/{locality}/{unit}'

def delete_directories(root):
    for name,directories,files in os.walk(root,topdown=False):
        for directory in directories:
            if not os.listdir(os.path.join(name,directory)):
                os.rmdir(os.path.join(name,directory))

