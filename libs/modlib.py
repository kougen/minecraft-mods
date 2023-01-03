import os
import shutil
import requests
from multipledispatch import dispatch

mod_conf = 'config/mods.conf.loc'

def create(data: str) -> tuple[str, str, str]:
    mod_dir, domain, mod_data = data.split(' ')[0], data.split(' ')[1], data.split(' ')[2]
    mod_name = mod_data.split('/')[2]
    link = f"https://{domain}.forgecdn.net/files/{mod_data}"
    return mod_name, mod_dir, link


class Mod:
    def __init__(self, name: str, mod_dir: str, link: str, mod_path: str):
        self.link = link
        self.name = name
        self.dir = mod_dir
        self.path = mod_path
        self.local_path = os.path.join('mods', self.dir, self.name)
        self.full_path = os.path.join(self.path, self.name)

    @classmethod
    def create_from_str(cls, data: str, destination_path: str) -> 'Mod':
        name, mod_dir, link = create(data)
        mod_path = destination_path
        return cls(name.strip(), mod_dir.strip(), link, mod_path)

    def __str__(self):
        return f"Mod: {self.name}\n\t-> {self.dir}\n\t-> {self.path}\n\t-> {self.link}"

    def organised_path(self):
        return os.path.join(self.path, self.dir, self.name)

    def in_game_path(self):
        return os.path.join(self.path, self.name)

    def download(self, organised: bool) -> bool:
        if organised:
            full_path = os.path.join(self.path, self.dir, self.name)
            if not os.path.exists(os.path.join(self.path, self.dir)):
                os.makedirs(os.path.join(self.path, self.dir))
        else:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            full_path = os.path.join(self.path, self.name)

        if not os.path.exists(full_path):
            try:
                print(f'Downloading: {self.name}')
                r = requests.get(self.link, allow_redirects=True)
                open(full_path, 'wb').write(r.content)
                return True
            except requests.exceptions.HTTPError as err:
                print(f'Download failed for: {self.link}')
                print(err)
                return False


@dispatch(str)
def read_mods(path: str) -> list[Mod]:
    mod_list = []
    with open(mod_conf, 'r') as mds:
        for m in mds:
            m = m.strip()
            if m != '' and m[0] != "#":
                mod_list.append(Mod.create_from_str(m, path))
    return mod_list


@dispatch(str, str)
def read_mods(path: str, lib: str) -> list[Mod]:
    mod_list = []
    with open(mod_conf, 'r') as mds:
        for m in mds:
            m = m.strip()
            if m != '' and m[0] != "#":
                mod = Mod.create_from_str(m, path)
                if mod.dir == lib:
                    mod_list.append(mod)
    return mod_list


def get_old_mod_list(path: str) -> set[str]:
    return set(os.listdir(path))


def get_new_mod_list(mods: list[Mod]) -> set[str]:
    new_mod_list = []
    for mod in mods:
        new_mod_list.append(mod.name)
    return set(new_mod_list)


def get_mod_by_name(name: str, mods: list[Mod]) -> Mod:
    for mod in mods:
        if name == mod.name:
            return mod


def delete_diff(old: list[str], new: list[str]) -> set[str]:
    new = set(new)
    old = set(old)
    return old - new


def download_diff(old: list[str], new: list[str]) -> set[str]:
    new = set(new)
    old = set(old)
    return new - old


def refresh_mods(old: list[str], new: list[str], path: str, is_organised: bool):
    for mod in delete_diff(old, new):
        print(f'Removing: {mod}')
        os.remove(os.path.join(path, mod))
    for mod in download_diff(old, new):
        if not os.path.exists(os.path.join(path, mod)):
            rel_path = get_mod_by_name(mod, read_mods(path)).local_path
            print(f"Copying: {rel_path} -> {path}")
            shutil.copy(rel_path, path)

