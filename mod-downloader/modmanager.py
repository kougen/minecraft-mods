import json
import os

from baselib import init

from newmod import Mod


class ModManager:
    mod_list = []  # type: list[Mod]
    mod_categories = []

    def __init__(self, json_dir: str, is_local=False):
        if len(self.mod_list) > 0:
            raise Exception
        init(is_local)
        for file in os.listdir(json_dir):
            if file.endswith('.json'):
                file_path = os.path.join(json_dir, file)
                json_data = open(file_path, 'r').read()
                mods_data = json.loads(json_data)
                for mod_data in mods_data:
                    category = file.replace('.json', '')
                    mod = Mod.load_from_json(mod_data, category)
                    if mod:
                        self.mod_list.append(mod)
                        # if not os.path.exists(mod.local_path) and mod.state != "inactive":
                        #     mod.download()
                        if category not in self.mod_categories:
                            self.mod_categories.append(category)

        for mod_obj in self.mod_list:
            temp = []
            for mod_str in mod_obj.depend_on_str:
                temp.append(self.get_mod_by_id(mod_str))
            mod_obj.depend_on = temp
