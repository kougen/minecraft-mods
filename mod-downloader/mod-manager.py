from pick import pick
from mod import Mod, ModPack, ModManager, pack_mods, unpack_mods

mods = ModManager(True)

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