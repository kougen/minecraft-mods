from pick import pick
from mod import Mod, ModPack, ModManager


def confirm(message: str) -> int:
	answer, i = pick(['Yes', 'No', 'Quit'], message, indicator='=>', default_index=0)
	return i


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


mods = ModManager(True)

operation, i = pick(['Add/Remove Mod', 'Edit Mod dependency', 'Pack the mods', 'Unpack the mods', 'Manage packs'], 'Choose an operation: ', indicator='=>', default_index=0)

if i == 1:
	operation, i = pick(['Add Dependency', 'Remove Dependency', 'Edit All'], 'Choose an operation: ', indicator='=>', default_index=0)
	if i == 2:
		stop = 0
		selected_mods = []  #type: list[Mod]
		while stop != 1:
			category, i = pick(mods.mod_categories, "Choose a category:", indicator='=>')
			stop = category
			choosen_mods = pick(mods.get_mods_by_category(category), multiselect=True, indicator='=>')
			for mod, index in choosen_mods:
				if mod in mods.mod_list and mod not in selected_mods:
					selected_mods.append(mod)
			stop = confirm('Continue selecting?')
		print("Please enter a list of dependencies: ")

		stop = 0
		selected_deps = []  #type: list[Mod]
		while stop != 1:
			category, i = pick(mods.mod_categories, "Choose a category:", indicator='=>')
			stop = category

			choosen_mods = pick(mods.get_mods_by_category(category), multiselect=True, indicator='=>')
			for dep, index in choosen_mods:
				if dep in mods.mod_list and dep not in selected_deps:
					selected_deps.append(dep)
			stop = confirm('Continue selecting?')

		dependency_list = []  #type: list[str]

		for dependency in selected_deps:
			if dependency in mods.mod_list:
				dependency_list.append(dependency.mod_id)
		print(dependency_list)

		for mod in selected_mods:
			mod.depend_on = mods.mod_id_list_to_mod(dependency_list)
		mods.mod_to_json()
elif i == 4:
	operation, i = pick(['Create', 'Edit', 'Remove'], 'Choose an operation: ', indicator='=>', default_index=0)
	if i == 0:
		pack = ModPack.create_pack()
		selected_mods = pick(mods.mod_list, 'Choose a mod: ', indicator='=>', multiselect=True)
		for mod, i in selected_mods:
			if mod.state == "install":
				pack.pack_content.append(mod)
		mods.mod_packs.append(pack)
		mods.packs_to_json()
	elif i == 1:
		pack, i = mods.select_mod_packs()
		operation, i = pick(['Name', 'Display Name', 'Description', 'Content'], 'What do you want to modify?', indicator='=>')
		if i == 3:
			operation, i = pick(['Add', 'Edit', 'Remove'], 'Choose an operation for the content: ',	indicator='=>')
			if i == 0:
				diff = set(mods.mod_list) - set(pack.pack_content)
				selected_mods = pick(list(diff), 'Choose a mod: ', indicator='=>', multiselect=True)
				for mod, i in selected_mods:
					if mod.state == "install":
						pack.pack_content.append(mod)
				mods.packs_to_json()
