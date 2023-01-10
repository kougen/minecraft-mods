import os
import shutil
import requests
from baselib import is_downloadable, create_dir, proj_root, curr_dir, clear_dir, minecraft_path
from globals import *
from typing import List
import json
from zipfile import ZipFile
from pick import pick
from termcolor import colored


zip_url = "https://github.com/joshika39/minecraft-mods/raw/main/data/mods.zip"
pack_url = "https://raw.githubusercontent.com/joshika39/minecraft-mods/main/mod-downloader/config/packs.json"

zip_path = os.path.join(proj_root(), 'data', 'mods.zip')
json_dir = os.path.join(proj_root(), 'data', 'mods')
mod_file_dir = os.path.join(proj_root(), 'data', 'jars')
pack_path = os.path.join(proj_root(), 'data', 'packs.json')
dev_pack_path = os.path.join(proj_root(), 'mod-downloader', 'config', 'packs.json')


def init(is_local=False):
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


def download_config():
    r = requests.get(zip_url, allow_redirects=True)
    open(zip_path, 'wb').write(r.content)
    r = requests.get(pack_url, allow_redirects=True)
    open(pack_path, 'wb').write(r.content)


def pack_mods():
    mods_path = os.path.join(proj_root(), 'mod-downloader', 'config', 'mods')
    with ZipFile(zip_path, 'w') as zip_obj:
        for mod in os.listdir(mods_path):
            file_path = os.path.join(mods_path, mod)
            if os.path.exists(file_path) and file_path.endswith('.json'):
                zip_obj.write(file_path, mod)


def unpack_mods():
    if not os.path.exists(zip_path):
        download_config()
    with ZipFile(zip_path, 'r') as zip_obj:
        path = os.path.join(proj_root(), 'data', 'mods')
        create_dir(path)
        os.chdir(path)
        zip_obj.extractall()


def remove_numbers(filename: str):
    return ''.join([i for i in filename if not i.isdigit()])


def remove_special(filename: str):
    return ''.join([i for i in filename if i.isalnum() or i == name_separator])


def construct_name(name: str):
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


def link_id(mod_id: str) -> str:
    if len(mod_id) == 7:
        result = ""
    while mod_id:
        result += f'{int(mod_id[:4])}/'
        mod_id = mod_id[4:]
    return result


class Mod:
    depend_on = []  # type: list['Mod']

    @classmethod
    def load_from_json(cls, json, category: str) -> 'Mod':
        return cls(json['id'], category, json['domain'], json['filename'], json['depend_on'], json['state'])

    def __str__(self):
        deps = ""
        for mod in self.depend_on:
            deps += f'{mod.name} '
        deps = deps[:-1]
        deps = deps[:75] + (deps[75:] and '..')
        return f"({self.name} {deps})"

    def details(self) -> str:
        return f"Mod: {self.name}\n-> {self.category}\n-> {self.filename}\n-> {self.link}\n" + 10 * '-' + '\n'

    def __init__(self, mod_id: str, category: str, domain: str, file_name: str, depend_on_str: list[str], state: str):
        self.state = state
        self.mod_id = mod_id
        self.category = category
        self.filename = file_name.replace(' ', '')
        self.domain = domain
        self.name = construct_name(self.filename)
        self.depend_on_str = depend_on_str
        self.local_dir = os.path.join(mod_file_dir, self.category)
        self.local_path = os.path.join(mod_file_dir, self.category, self.filename)
        if state != 'inactive' or state == "download":
            self.link = f'https://{self.domain}.forgecdn.net/files/{link_id(mod_id)}{self.filename}'
            if os.path.exists(self.local_dir) and os.path.exists(self.local_path):
                self.download()

    def depend_on_to_str(self) -> list[str]:
        data = [dep.mod_id for dep in self.depend_on]
        return data

    def serializable_attrs(self):
        props = {'id': self.mod_id, 'domain': self.domain, 'filename': self.filename,
                 'depend_on': self.depend_on_to_str(),
                 'state': self.state}
        return props

    def download(self) -> bool:
        if not os.path.exists(self.local_path):
            create_dir(self.local_dir)
            try:
                if is_downloadable(self.link):
                    print(f'Downloading: {self.name}\n[TO]: {self.local_path}\n[FROM]: {self.link}')
                    r = requests.get(self.link, allow_redirects=True)
                    open(self.local_path, 'wb').write(r.content)
                    return True
                else:
                    print(f'Download failed for: {self.link}')
                    return False
            except requests.exceptions.HTTPError as err:
                print(f'Download failed for: {self.link}')
                print(err)
                return False

    def copy2(self, path: str):
        dest = os.path.join(path, self.filename)
        if os.path.exists(self.local_dir) and os.path.exists(self.local_path):
            if not os.path.exists(dest) and self.state == "install":
                shutil.copyfile(self.local_path, dest)
                print(f'Copying: {self.local_path} -> {dest}')
                if self.depend_on is not None and len(self.depend_on) > 0:
                    for dep in self.depend_on:
                        dep.copy2(path)
        else:
            print(f"Local mod not found: {self.local_path}")

    def remove(self):
        print(f"Removing: {self.local_path}")
        os.remove(os.path.join(mod_file_dir, self.local_path))


class ModPack:

    @classmethod
    def load_from_json(cls, pack_json, pack_content: List[Mod]) -> 'ModPack':
        return cls(pack_json['name'], pack_json['display_name'], pack_json['description'], pack_content)

    @classmethod
    def create_pack(cls) -> 'ModPack':
        name = input('Enter a pack name: ')
        display_name = input('Enter a display name: ')
        description = input('Enter a description: ')
        return cls(name, display_name, description, [])

    def __init__(self, name: str, display_name: str, description: str, pack_content: List[Mod]):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.pack_content = pack_content

    def __str__(self) -> str:
        contents = ""
        for mod in self.pack_content:
            contents += f'{mod.name} '
        contents = contents[:-1]
        contents = contents[:75] + (contents[75:] and '..')
        return f'{self.display_name} ({self.name}) ~ {self.description} | Contents: [{contents}]'
        # return colored(f'{self.display_name}', ) + f'({self.name}) ~ ' + colored(f'{self.description}', 'green', attrs=['bold']) + f' | Contents: [{contents}]'

    def serializable_attrs(self):
        props = {'name': self.name, 'display_name': self.display_name, 'description': self.description,
                 'pack_content': [i.mod_id for i in self.pack_content]}
        return props


def installed_mods_list() -> list[str]:
    mods = []
    if os.path.exists(mod_file_dir):
        for folder in os.listdir(mod_file_dir):
            folder_path = os.path.join(mod_file_dir, folder)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.exists(file_path) and file.endswith('.jar'):
                        mods.append(file)
    return mods


class ModManager:
	mod_list = []  # type: List[Mod]
	mod_categories = []
	mod_packs = []  # type: List[ModPack]

	def __init__(self, is_local=False):
		if len(self.mod_list) > 0:
			raise Exception
		init(is_local)
		for file in os.listdir(json_dir):
			if file.endswith('.json'):
				file_path = os.path.join(json_dir, file)
				json_data = open(file_path, 'r').read()
				mods_data = json.loads(json_data)
				for mod_data in mods_data:
					category = file.replace('.json', '')
					mod = Mod.load_from_json(mod_data, category)
					if mod:
						self.mod_list.append(mod)
						if not os.path.exists(mod.local_path) and mod.state != "inactive":
							mod.download()
						if category not in self.mod_categories:
							self.mod_categories.append(category)

		for mod_obj in self.mod_list:
			temp = []
			for mod_str in mod_obj.depend_on_str:
				temp.append(self.get_mod_by_id(mod_str))
			mod_obj.depend_on = temp
		self.mod_packs = self.get_mod_packs()

	def __del__(self):
		self.mod_list.clear()
		self.mod_packs.clear()
		self.mod_categories.clear()

	def print(self):
		for mod in self.mod_list:
			print(mod)

	def packs_to_json(self):
		data = []
		for pack in self.mod_packs:
			data.append(pack.serializable_attrs())
		json_obj = json.dumps(data, indent=4)
		with open(dev_pack_path, "w") as outfile:
			outfile.write(json_obj)

	def mod_to_json(self):
		for category in self.mod_categories:
			target = os.path.join(curr_dir(), 'config', 'mods', f'{category}.json')
			data = []
			for mod in self.mod_list:
				if mod.category == category:
					data.append(mod.serializable_attrs())

			json_object = json.dumps(data, indent=4)

			with open(target, "w") as outfile:
				outfile.write(json_object)
			print(f'{category} category done')

	def search(self, search_string: str) -> list[Mod]:
		results = []
		for mod in self.mod_list:
			if mod.state != "inactive" and (search_string in mod.name
											or search_string in mod.category
											or search_string in mod.link
											or search_string in mod.filename):
				results.append(mod)
		return results

	def get_mod_packs(self) -> list[ModPack]:
		mod_packs = []  # type: list[ModPack]
		if os.path.exists(pack_path):
			json_data = open(pack_path, 'r').read()
			packs = json.loads(json_data)
			for pack_data in packs:
				temp_mods = []  # type: list[Mod]
				for mod_id in pack_data['pack_content']:
					if self.get_mod_by_id(mod_id) is not None:
						temp_mods.append(self.get_mod_by_id(mod_id))
				mod_packs.append(ModPack.load_from_json(pack_data, temp_mods))
			return mod_packs

	def select_mod_packs(self) -> tuple[ModPack, int]:
		if self.mod_packs is not None:
			chosen = pick(self.mod_packs, "Select a mod pack:")  # type: tuple[ModPack, int]
			return chosen

	def get_pack_content_by_name(self, name):
		for pack in self.mod_packs:
			if pack == name:
				return pack

	def get_mods_by_category(self, category: str) -> list[Mod]:
		mod_list = []
		for mod in self.mod_list:
			if mod.state == "install" and mod.category == category:
				mod_list.append(mod)
		return mod_list

	def get_mod_by_name(self, name: str) -> Mod:
		for mod in self.mod_list:
			if mod.name == name:
				return mod

	def get_mod_by_filename(self, filename: str) -> Mod:
		for mod in self.mod_list:
			if mod.filename == filename:
				return mod

	def get_mod_by_id(self, id: str) -> Mod:
		for mod in self.mod_list:
			if mod.mod_id == id:
				return mod

	def mod_id_list_to_mod(self, ids: list[str]) -> List[Mod]:
		return [self.get_mod_by_id(_mod_id) for _mod_id in ids]