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