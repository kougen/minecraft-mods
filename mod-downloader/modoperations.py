from mod import Mod, ModManager, init, installed_mods_list
import os
from baselib import *


def update_mods(mods: ModManager, is_local=False):
    init(is_local)
    for mod in mods.mod_list:
        if mod.state != "inactive" and not os.path.exists(mod.local_path):
            mod.download()

    for mod_file in installed_mods_list():
        mod = mods.get_mod_by_filename(mod_file)
        if mod not in mods.mod_list or mod.state == "inactive":
            mod.remove()


def refresh_mods(mods: ModManager, path: str):
    for mod in mods.mod_list:
        mod.copy2(path)

    for mod_file in os.listdir(path):
        mod = mods.get_mod_by_filename(mod_file)
        mod_path = os.path.join(path, mod_file)
        if mod.filename not in installed_mods_list() or mod.state != "install":
            print(f"Removing: {mod_path}")
            os.remove(mod_path)


def copy_to_target(manager: ModManager, pack_mods: list[Mod], path: str):
    for mod_file in os.listdir(path):
        result = manager.get_mod_by_filename(mod_file)
        dep_mods = []

        for mod in pack_mods:
            for dep in mod.depend_on:
                if dep not in dep_mods:
                    dep_mods.append(dep)

        if result is not None:
            mod_path = os.path.join(path, mod_file)
            if result.filename not in installed_mods_list() or result not in pack_mods or result.state != "install":
                if result not in dep_mods:
                    print(f"Removing: {mod_path}")
                    os.remove(mod_path)

    for pack_mod in pack_mods:
        pack_mod.copy2(path)
