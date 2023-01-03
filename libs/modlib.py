import os
import requests


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


def read_mods(path: str) -> list[Mod]:
    mod_list = []
    with open('config/mods.conf', 'r') as mds:
        for m in mds:
            m = m.strip()
            if m != '' and m[0] != "#":
                mod_list.append(Mod.create_from_str(m, path))
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
