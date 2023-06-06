import io
import os
import UnityPy
import json

src = "./JPMasters"
src = "../output"
#src = "C:\\Users\\Arctia\\AppData\\LocalLow\\disgaearpg\\DisgaeaRPG\\assetbundle\\masters\\"
env = UnityPy.load(src)
#extract_dir = "C:\\Users\\Arctia\\Desktop\\Root\\Projects\\DRPG_Wiki\\datas\\JP"
extract_dir = "./JPTranslated"

for obj in env.objects:
    if obj.type.name == "MonoBehaviour":
        # export
        if obj.serialized_type.nodes:
            # save decoded data
            data = obj.read()
            tree = obj.read_typetree()
            fp = os.path.join(extract_dir, f"{data.name}.json")
            with open(fp, "wt", encoding = "utf8") as f:
                json.dump(tree, f, ensure_ascii = False, indent = 4)
        else:
            # save raw relevant data (without Unity MonoBehaviour header)
            data = obj.read()
            fp = os.path.join(extract_dir, f"{data.name}.bin")
            with open(fp, "wb") as f:
                f.write(data.raw_data)
        print(data.name)
        # edit
        if obj.serialized_type.nodes:
            tree = obj.read_typetree()
            # apply modifications to the data within the tree
            obj.save_typetree(tree)
        else:
            with open(replace_dir, data.name) as f:
                data.save(raw_data = f.read())
