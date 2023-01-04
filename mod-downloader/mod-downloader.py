from mod import ModManager
from baselib import clear_dir, minecraft_path
from modoperations import copy_to_target

manager = ModManager()
pack, i = manager.select_mod_packs()

copy_to_target(manager, pack.pack_content, minecraft_path())

input("Press Enter to exit...")
