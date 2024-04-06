
import os, json, shutil
import UnityPy, dotenv

dotenv.load_dotenv("../.env")

intermediate = ""
if os.getenv("DRPG_DEFAULT_PATH") == "true":
    try:
        intermediate = os.path.join(
            os.getenv('LOCALAPPDATA'), "..",
            "LocalLow", "disgaearpg", "DisgaeaRPG", 
            "assetbundle", "masters")
    except Exception as e:
        print(f"[ERROR ]: Failed to find Master folder -> {e}")
else:
    intermediate = os.getenv("DRPGMasters_path")

files_to_export = [
    "character",
    "charactercommand",
    "characterretrofit",
    "charactermagiccommand",
    "command",
    "leaderskill",
    "characterclassname",
    "ritualtrainings",
    "necessaryrebirthmaterial"
]

src = "./JPNeeded"

for file in files_to_export:
    shutil.copy2(os.path.join(intermediate, file), os.path.join(src, file))

# src = "./JPMasters"
env = UnityPy.load(src)

extract_dir = "JP"

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
        print("[INFO  ]: done ", data.name)
        # edit
        if obj.serialized_type.nodes:
            tree = obj.read_typetree()
            # apply modifications to the data within the tree
            obj.save_typetree(tree)
        # else:
            # with open(replace_dir, data.name) as f:
                # data.save(raw_data = f.read())
