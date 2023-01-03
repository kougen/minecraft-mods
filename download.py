from sys import platform
from pathlib import Path
from pick import pick

from libs.modlib import *


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


if platform == "linux" or platform == "linux2":
    target_path = str(Path.home())
elif platform == "darwin":
    target_path = str(Path.home())
elif platform == "win32":
    target_path = str(os.getenv('APPDATA'))
else:
    exit("Unknown platform")

target_path = os.path.join(target_path, ".minecraft", "mods")


mode, mode_i = pick(['Update locally stored mods', 'Update mods on the pc'], 'Please choose your source: ',
                    indicator='=>', default_index=1)

if mode_i == 0:
    mods = read_mods('mods')
    for mod in mods:
        mod.download(True)

else:
    source, source_i = pick(['cdn', 'local'], 'Please choose your source: ', indicator='=>', default_index=1)
    target, target_i = pick(['server', 'client'], 'Please choose your target: ', indicator='=>', default_index=1)
    is_fresh, is_fresh_i = pick(['Yes', 'No'], 'Do you want a fresh install: ', indicator='=>', default_index=1)
    is_backup, is_backup_i = pick(['Yes', 'No'], 'Do you want to backup the old mods: ', indicator='=>')

    if target_i == 0:
        while not os.path.exists(target_path):
            target_path = input('Enter the server mod folder path: ')
            if not os.path.exists(target_path):
                print('Server mod folder path does not exist!')
        
    if is_fresh_i == 0:
        os.remove(os.path.join(target_path, '*.jar'))
        
    old_mods = get_old_mod_list(target_path)
    new_mods = get_new_mod_list(read_mods(target_path))
    for mod in old_mods - new_mods:
        print(f'Removing: {mod}')
        os.remove(os.path.join(target_path, mod))
    for mod in new_mods - old_mods:
        get_mod_by_name(mod, read_mods(target_path)).download(False)

