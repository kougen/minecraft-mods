from pathlib import Path
import os
from sys import platform


def curr_dir() -> str:
	return os.path.dirname(os.path.realpath(__file__))

def proj_root() -> str:
	temp = Path(curr_dir())
	return str(temp.parent)


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
