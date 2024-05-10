from mod import Mod, ModPack, ModManager, PackManager, pack_mods, unpack_mods
from advanced_selector import SingleMenu, MultiMenu, MenuWrapper, FunctionItem
import os
import time
from baselib import is_downloadable

DEFAULT_IMPORT_PATH = 'modimport.txt'
MOD_SEPARATOR = ';'

mod_manager = ModManager(True)
pack_manager = PackManager(mod_manager, True)


def remove_selected_mods(selected_mods):
    for mod in selected_mods:
        if mod in mod_manager.mod_list:
            mod_manager.mod_list.remove(mod)


def add_single_mod():
    mod_id = input("Enter mod id: ")
    mod_category = input("Mod category: ")
    mod_domain = input("Domain (default:mediafilez): ")
    if mod_domain == "":
        mod_domain = "mediafilez"
    mod_filename = input("Filename: ")
    mod_state = input("State (default:install): ")
    if mod_state == "":
        mod_state = "install"
    mod_deps = input("Dependencies: ")
    deps = []
    deps = mod_deps.split(' ')
    mod =  Mod(mod_id, mod_category, mod_domain, mod_filename, deps, mod_state)
    link = mod.link
    if is_downloadable(link):
        mod_manager.mod_list.append(mod)
    else:
        print("Mod is not downloadable")
        print(f"Link is: {link}")
        time.sleep(2)
    mod_manager.mod_to_json()


def add_single_pack():
    pack_name = input("Enter pack name: ")
    pack_dis_name = input("Enter pack display name: ")
    pack_desc = input("Enter pack description: ")
    contents = MultiMenu("Contents:", mod_manager.mod_list).show()  # type: list[Mod]
    pack = ModPack.create_pack(pack_name, pack_dis_name, pack_desc, contents)
    if pack is not None:
        pack_manager.mod_packs.append(pack)
        pack_manager.packs_to_json()


def add_multiple_mod():
    global DEFAULT_IMPORT_PATH
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
        if mod not in mod_manager.get_mod_filenames():
            mod_manager.mod_list.append(mod)


def list_contents(selected):
    os.system('cls')
    pack = ModPack.init_pack(selected)
    mod_count, category_dict = pack.list_contents_ordered(mod_manager.mod_categories, ['install'])
    print(f"Mod count in the pack: {mod_count}")
    for category in category_dict:
        print(f'---{category.upper()}---')
        for mod in category_dict[category]:
            print(f'{mod}')
    input('Press any key to continue...')


def modify_mod_state():
    valid_states = ['install', 'download', 'inactive']
    state = SingleMenu("New State:", valid_states).show()
    if state in valid_states:
        mods = MultiMenu("Select this mods", mod_manager.mod_list).show()  # type: list[Mod]
        for mod in mods:
            mod.state = state
    mod_manager.mod_to_json()


def add_deps_to_mod():
    target_mod = SingleMenu("Mod to modify", mod_manager.mod_list).show()  # type: Mod
    if target_mod is not None:
        deps = MultiMenu("Dependencies", mod_manager.mod_list).show() # type: list[Mod]
        if deps is not None:
            for dep in deps:
                if dep not in target_mod.depend_on:
                    target_mod.depend_on.append(dep)
            mod_manager.mod_to_json()


def modify_mod_dependencies():
    target_mods = MultiMenu("Target mods", mod_manager.mod_list).show()


def add_mod_to_mod_pack():
    pack = SingleMenu("Select a modpack", pack_manager.mod_packs).show()  #type: ModPack
    if pack is not None:
        deps = []
        for mod in pack.pack_content:
            for dep in mod.depend_on:
                if dep not in deps:
                    deps.append(dep)

        available_mods = set(mod_manager.mod_list) ^ set(pack.pack_content) ^ set(deps)
        if len(available_mods) <= 0:
            print("No mods available")
            time.sleep(3)
            return
        selection = MultiMenu("Select the mods:", list(available_mods)).show()
        if len(selection) == 1:
            pack.pack_content.append(selection)
        else:
            for mod in selection:
                pack.pack_content.append(mod)
        pack_manager.packs_to_json()


def remove_mod_from_mod_pack():
    pack = SingleMenu("Select a modpack", pack_manager.mod_packs).show()  #type: ModPack
    if pack is not None:
        selection = MultiMenu("Select the mods:", pack.pack_content).show()
        pack.remove_mods(selection)
        pack_manager.packs_to_json()


def sos_function():
    for mod in mod_manager.new_mod_list:
        print(mod)
        mod.save()
    _ = input("press any key to continue")


main_menu = MenuWrapper(
    "Select Operation", [
        MenuWrapper("Select mod Operation", [
            FunctionItem("Add Single Mod", add_single_mod),
            FunctionItem("Add Multiple Mod", add_multiple_mod),
            FunctionItem("Modify mod state", modify_mod_state),
            FunctionItem("List all mods", mod_manager.print),
            MenuWrapper("Mod Dependencies", [
                FunctionItem("Add Deps", add_deps_to_mod),
                FunctionItem("Remove Deps", remove_mod_from_mod_pack),
                FunctionItem("Edit Deps", modify_mod_dependencies)
            ]),
            FunctionItem("Pack mods", pack_mods),
            FunctionItem("Unpack mods", unpack_mods)
        ]),
        MenuWrapper("Select pack Operation", [
            FunctionItem("Create a pack", add_single_pack),
            SingleMenu("List Pack Content", pack_manager.mod_packs, list_contents),
            MenuWrapper("Modify Pack Content", [
                FunctionItem("Add Mod", add_mod_to_mod_pack),
                FunctionItem("Remove Mod", remove_mod_from_mod_pack),
            ]),
        ]),
        FunctionItem("Sos", sos_function)
])

main_menu.show()
