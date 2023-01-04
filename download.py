from sys import platform
import argparse
from pathlib import Path
from pick import pick

from libs.modlib import *

r = requests.get("https://raw.githubusercontent.com/joshika39/minecraft-mods/main/config/mods.conf", allow_redirects=True)
if os.path.exists(mod_conf):
    os.remove(mod_conf)
if not os.path.exists('config'):
    os.mkdir('config')
    os.mkdir('mods')
open(mod_conf, 'wb').write(r.content)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--server', '-s', action='store_true')
group.add_argument('--client', '-c', action='store_true')
group.add_argument('--localmods', '-l', action='store_true')
group.add_argument('--reset', '-r', action='store_true')
group.add_argument('--clear', action='store_true')
args = parser.parse_args()

if platform == "linux" or platform == "linux2":
    target_path = str(Path.home())
elif platform == "darwin":
    target_path = str(Path.home())
elif platform == "win32":
    target_path = str(os.getenv('APPDATA'))
else:
    exit("Unknown platform")


def update_local_files(is_local_conf: bool):
    mods = read_mods('mods', is_local_conf)
    folders = os.listdir('mods')
    for folder in folders:
        sub_path = os.path.join('mods', folder)

        old_mods = get_old_mod_list(sub_path)
        new_mods = get_new_mod_list(read_mods('mods', folder, is_local_conf))
        
        for mod in old_mods - new_mods:
            print(f'Removing from {sub_path}: {mod}')
            os.remove(os.path.join(sub_path, mod))
    for mod in mods:
        mod.download(True)


def delete_files(path: str, ext: str):
    test = os.listdir(path)
    for item in test:
        if item.endswith(ext):
            os.remove(os.path.join(path, item))

target_path = os.path.join(target_path, ".minecraft", "mods")

if args.localmods:
    update_local_files(True)
    exit(0)

if args.clear:
    for folder in os.listdir('mods'):
        path = os.path.join('mods', folder) 
        delete_files(path, ".jar")
        os.rmdir(path)
    delete_files(target_path, ".jar")
    exit(0)

if args.reset:
    if os.path.exists(mod_conf_local):
        if os.path.exists(mod_conf):
            os.remove(mod_conf)
        shutil.copyfile(mod_conf_local, mod_conf)
    exit(0)

if args.server:
    target_path = ""
    update_local_files(False)
    mods = []
    while not os.path.exists(target_path):
        target_path = input('Enter the server mod folder path: ')
        if not os.path.exists(target_path):
            print('Server mod folder path does not exist!')
    if os.path.exists('mods'):
        for folder in os.listdir('mods'):
            path = os.path.join('mods', folder)
            mods.extend(os.listdir(path))
    server_mods = os.listdir(target_path)
    refresh_mods(server_mods, mods, target_path, False)
    exit(0)

if args.client:
    update_local_files(False)
    mods = []
    if os.path.exists('mods'):
        for folder in os.listdir('mods'):
            path = os.path.join('mods', folder)
            mods.extend(os.listdir(path))
    server_mods = os.listdir(target_path)
    refresh_mods(server_mods, mods, target_path, False)
    exit(0)

# mode, mode_i = pick(['Update locally stored mods', 'Update mods on the pc'], 'Please choose your source: ', indicator='=>', default_index=1)



