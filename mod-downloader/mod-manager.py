from pick import pick
from mod import Mod, ModPack, ModManager, pack_mods, unpack_mods
from typing import Any, List, Optional, Sequence, Callable


menu = (['Add/Remove Mod', 'Edit Mod dependency', 'Pack the mods', 'Unpack the mods', 'Manage packs'],
        'Choose an operation: ',
        False, True)
menu_1 = (['Add Dependency', 'Remove Dependency', 'Edit All'],
          'Choose an operation: ', True, True)
menu_2 = ['Add/Remove Mod', 'Edit Mod dependency',
          'Pack the mods', 'Unpack the mods', 'Manage packs']


def confirm(message: str) -> int:
    return pick((['Yes', 'No', 'Quit'], message, False, True))


mods = ModManager(True)


class MenuItem():
    def __init__(self, content, callback: Callable = None, submenu: 'Menu' = None):
        self.content = content
        self.callback = callback
        self.submenu = submenu

    def __str__(self):
        return self.content


class Menu():
    def __init__(self, options: list[MenuItem], title="Menu:"):
        self.options = options
        self.title = title

    def pick(self) -> tuple[MenuItem, int]:
        return pick(self.options, self.title)

    def show(self):
        selected, i = self.pick()
        if selected.callback is not None:
            selected.callback()
        if selected.submenu is not None:
            selected.submenu.show()


def select_one_mod():
    result_count = 0
    while result_count != 1:
        mod_name = input("Mod name: ")
        mod_res = mods.search(mod_name)
        result_count = len(mod_res)
        if result_count > 1:
            print("Please narrow your seach:")
            for i in mod_res:
                print(f"\t{i.name}")
    return mod_res[0]


def add_mods_to_pack():
    pack, i = mods.select_mod_packs()
    diff = set(mods.mod_list) - set(pack.pack_content)
    selected_mods = pick(list(diff), 'Choose a mod: ', indicator='=>', multiselect=True)
    for mod, i in selected_mods:
        if mod.state == "install":
            pack.pack_content.append(mod)
    mods.packs_to_json()


def edit_mods_in_pack():
    pack, i = mods.select_mod_packs()
    selected_mods = pick(mods.mod_list, 'Choose a mod: ', indicator='=>', multiselect=True)
    for mod, i in selected_mods:
        if mod.state == "install":
            pack.pack_content.append(mod)
    mods.packs_to_json()


def remove_mods_from_pack():
    pack, i = mods.select_mod_packs()
    selected_mods = pick(pack.pack_content, 'Choose a mod: ', indicator='=>', multiselect=True)
    for mod, i in selected_mods:
        pack.pack_content.remove(mod)
    mods.packs_to_json()


def create_pack():
    pack = ModPack.create_pack()
    selected_mods = pick(mods.mod_list, 'Choose a mod: ', indicator='=>', multiselect=True)
    for mod, i in selected_mods:
        if mod.state == "install":
            pack.pack_content.append(mod)
    mods.mod_packs.append(pack)
    mods.packs_to_json()


pack_content_menu = Menu(
    [
        MenuItem("Add", add_mods_to_pack),
        MenuItem("Edit", edit_mods_in_pack),
        MenuItem("Remove", remove_mods_from_pack)
    ], "Select a content operation"
)


pack_detail_menu = Menu(
    [
        MenuItem("Name"),
        MenuItem("Display Name"),
        MenuItem("Description"),
        MenuItem("Content", submenu=pack_content_menu),
    ], 'What do you want to modify?'
)


pack_menu = Menu(
    [
        MenuItem('Create Pack', create_pack),
        MenuItem('Edit Pack', submenu=pack_detail_menu),
        MenuItem('Remove Pack'),
    ], "Select a pack operation"
)

pack_menu.show()