from mod import Mod, ModPack, ModManager, pack_mods, unpack_mods
from picker import SingleMenu, MenuWrapper, MultiMenu, FunctionItem
import os

DEFAULT_IMPORT_PATH = 'modimport.txt'
MOD_SEPARATOR = ';'

manager = ModManager(True)

def select_one_mod():
    result_count = 0
    while result_count != 1:
        mod_name = input("Mod name: ")
        mod_res = manager.search(mod_name)
        result_count = len(mod_res)
        if result_count > 1:
            print("Please narrow your seach:")
            for i in mod_res:
                print(f"\t{i.name}")
    return mod_res[0]


def remove_selected_mods(selected_mods):
    for mod in selected_mods:
        if mod in manager.mod_list:
            manager.mod_list.remove(mod)

def add_single_mod():
    mod_id = input("Enter mod id: ")
    mod_domain = input("Domain: ")
    mod_filename = input("Filename: ")

def add_multiple_mod():
    if not os.path.exists(DEFAULT_IMPORT_PATH):
        print("Default file not found: " + DEFAULT_IMPORT_PATH)
        DEFAULT_IMPORT_PATH = input("Enter filepath")
    file = open(DEFAULT_IMPORT_PATH, 'r')
    lines = file.readlines()
    category = lines[0]
    for i in range(1, len(lines)):
        line = lines[i]
        data = line.split(MOD_SEPARATOR)
        mod = Mod(data[0], category, data[1], data[3], [], data[2])
        if mod not in manager.get_mod_filenames():
            manager.mod_list.append(mod)

def list_contents(selected):
    pack = ModPack.init_pack(selected)
    pack.list_contents()
    input('Press any key to continue...')

pack_menu = MenuWrapper("Select pack Operation", [
    SingleMenu("List Pack Content", manager.mod_packs, list_contents)
])

main_menu = MenuWrapper(
    "Select Operation", [
        FunctionItem("Add Single Mod", add_single_mod),
        FunctionItem("Add Multiple Mod", add_multiple_mod),
        pack_menu
])
main_menu.show()