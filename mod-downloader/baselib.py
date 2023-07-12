from zipfile import ZipFile
import requests
import os, shutil
from sys import platform
from globals import mod_separator
from pathlib import Path

def get_path(pathname: str) -> str:
	target_path = ""
	while not check_path(target_path):
			target_path = input(f'Enter the {pathname} path: ')
			if not check_path(target_path):
				print(f'{pathname.capitalize()} path does not exist!')
	return target_path

def curr_dir() -> str:
	return os.path.dirname(os.path.realpath(__file__))


def proj_root() -> str:
	temp = Path(curr_dir())
	return str(temp.parent)


def is_data_valid(data: str) -> list:
	data = data.strip()
	if data == '' or data.startswith("#") or data.endswith('!'):
		return [False]

	for i in range(4, 1, -1):
		data = data.replace(mod_separator*i, mod_separator)

	path_info = data.split(mod_separator)
	if len(path_info) < 4:
		return [False]
	else:
		return [True, data]


def is_downloadable(request) -> bool:
	response = requests.head(request)
	if response.status_code == 200:
		return True
	else:
		return False


def create_dir(path: str):
	if not os.path.exists(path):
		os.makedirs(path)


def clear_dir(path: str):
	for filename in os.listdir(path):
		file_path = os.path.join(path, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_home_path() -> str:
	if platform == "linux" or platform == "linux2":
		return str(Path.home())
	elif platform == "darwin":
		return str(Path.home())
	elif platform == "win32":
		return str(os.getenv('APPDATA'))
	else:
		exit("Unknown platform")


def minecraft_path() -> str:
	return os.path.join(get_home_path(), ".minecraft", "mods")


def check_path(path: str) -> bool:
	return os.path.exists(path)

def remove_numbers(filename: str):
    return ''.join([i for i in filename if not i.isdigit()])


def remove_special(filename: str, name_separator='-'):
    return ''.join([i for i in filename if i.isalnum() or i == name_separator])

def construct_name(name: str, name_separator='-'):
    name = remove_numbers(name)
    name = name.replace('-', name_separator)
    name = name.replace('_', name_separator)
    name = name.replace('reforged', '')
    name = name.replace('build', '')
    name = name.replace('forge', '')
    name = name.replace('version', '')
    name = name.replace('-v', '')
    name = name.replace('-mc', '')
    name = name.replace('.jar', '')
    name = remove_special(name)
    for i in range(5, 2, -1):
        name = name.replace(name_separator * i, name_separator)

    while name.endswith(name_separator):
        name = name[:-1]
    while name.startswith(name_separator):
        name = name[1:]
    return name.lower()

def download_config(zip_path: str, pack_path: str, pack_url: str, zip_url: str):
    r = requests.get(zip_url, allow_redirects=True)
    open(zip_path, 'wb').write(r.content)
    r = requests.get(pack_url, allow_redirects=True)
    open(pack_path, 'wb').write(r.content)


def pack_mods(zip_path: str):
    mods_path = os.path.join(proj_root(), 'mod-downloader', 'config', 'mods')
    with ZipFile(zip_path, 'w') as zip_obj:
        for mod in os.listdir(mods_path):
            file_path = os.path.join(mods_path, mod)
            if os.path.exists(file_path) and file_path.endswith('.json'):
                zip_obj.write(file_path, mod)


def unpack_mods(zip_path: str):
    if not os.path.exists(zip_path):
        download_config()
    with ZipFile(zip_path, 'r') as zip_obj:
        path = os.path.join(proj_root(), 'data', 'mods')
        create_dir(path)
        os.chdir(path)
        zip_obj.extractall()

def init(json_dir: str, mod_file_dir: str, dev_pack_path: str, pack_path: str, zip_path: str, is_local=False):
    create_dir(os.path.join(proj_root(), 'data'))
    create_dir(json_dir)
    create_dir(mod_file_dir)
    if is_local:
        clear_dir(json_dir)
        pack_mods()
        unpack_mods()
        shutil.copyfile(dev_pack_path, pack_path)
        if len(os.listdir(json_dir)) <= 0 or not os.path.exists(zip_path):
            download_config()
            unpack_mods()
    else:
        download_config()
        unpack_mods()