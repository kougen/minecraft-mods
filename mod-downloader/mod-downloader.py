from mod import ModManager
from baselib import minecraft_path
from modoperations import copy_to_target

manager = ModManager()
pack = manager.select_mod_packs()
if pack is not None:
	copy_to_target(manager, pack.pack_content, minecraft_path())
	input("Press Enter to exit...")

