import os
import time
from base import proj_root, minecraft_path, curr_dir, check_path
import shutil
from selection_picker_joshika39 import FunctionItem, MenuWrapper


def move_mods():
    current_mods = os.listdir(minecraft_path())
    for mod in current_mods:
        if os.path.exists(mod):
            target = os.path.join(current_mods, mod)
            print(f"Deleting {target}")
            os.remove(target)

    sources = os.path.join(curr_dir(), "src") 
    source_mods = os.listdir(sources)
    for source in source_mods:
        target_path = os.path.join(sources, source)
        print(f"Moving: {target_path}")
        shutil.copy2(target_path, minecraft_path())
    print("Finished moving!")
    time.sleep(3)


MenuWrapper("Select an operation", [
    FunctionItem("Move mods", move_mods)
]).show()




