from mod import ModManager, PackManager
from selection_picker_joshika39 import SingleMenu, MenuWrapper, FunctionItem
from baselib import minecraft_path, check_path, get_path, curr_dir, create_dir
from modoperations import copy_to_target
import json
import argparse
import os

create_dir(os.path.join(curr_dir(), 'config'))
prefs = os.path.join(curr_dir(), 'config', 'config.json')

parser = argparse.ArgumentParser()
parser.add_argument('--server', '-s', action='store_true', help='Copy the mods to the server\'s folder.')
args = parser.parse_args()

mod_mgr = ModManager()
pack_mgr = PackManager(mod_mgr)
pack = pack_mgr.select_mod_packs()

if args.server and pack is not None:
	def copy_to_path(path: str):
		if not check_path(path):
			print(f"Path not found: {path}")
		else:
			copy_to_target(mod_mgr, pack.pack_content, path)
		exit(0)
	
	def clear_prev_paths():
		json_data = open(prefs, 'r').read()
		properties = json.loads(json_data)
		properties['previous_server_paths'] = []
		json_object = json.dumps(properties, indent=4)
		with open(prefs, "w") as outfile:
			outfile.write(json_object)

	def new_server_path():
		path = get_path('server mod folder')
		json_data = open(prefs, 'r').read()
		properties = json.loads(json_data)
		prevs = properties['previous_server_paths']  # type: list[str]
		prevs.append(path)
		json_object = json.dumps(properties, indent=4)
		with open(prefs, "w") as outfile:
			outfile.write(json_object)
		copy_to_path(path)

	if not os.path.exists(prefs):
		path = get_path('server mod folder')
		properties = { "previous_server_paths": [path] }
		json_object = json.dumps(properties, indent=4)
		with open(prefs, "w") as outfile:
			outfile.write(json_object)
		copy_to_path(path)
	else:
		json_data = open(prefs, 'r').read()
		properties = json.loads(json_data)
		prev_paths = properties['previous_server_paths']  #type: list
		MenuWrapper("Choose a path:", [
				SingleMenu(f"Previous paths", prev_paths, callback=copy_to_path),
				FunctionItem("New Path", new_server_path),
				FunctionItem("Clear previous paths", clear_prev_paths)
			]).show()


		
else:
	if pack is not None:
		copy_to_target(mod_mgr, pack.pack_content, minecraft_path())

input("Press Enter to exit...")

