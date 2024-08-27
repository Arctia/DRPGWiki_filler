
import os, json, shutil
import UnityPy, dotenv

dotenv.load_dotenv(".env")


def get_master_path() -> str|None:
    mdir: str|None = None
    if os.getenv("DRPG_DEFAULT_PATH") == "true":
        try:
            mdir = os.path.join(
                os.getenv('LOCALAPPDATA'), "..",
                "LocalLow", "disgaearpg", "DisgaeaRPG", 
                "assetbundle", "masters")
        except Exception as e:
            print(f"[ERROR ]: Failed to find Master folder -> {e}")
            return None
    else:
        mdir = os.getenv("DRPGMasters_path")
    return mdir


def create_folders(dirs:list) -> None:
    for d in dirs:
        try:
            os.makedirs(d)
        except Exception as e:
            # print(f"[WARN  ]: dir <{d}> already exists")
            pass


def copy_files(src:str, mdir:str, dst:str) -> None:
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

    create_folders([src, dst])

    for file in files_to_export:
        shutil.copy2(os.path.join(mdir, file), os.path.join(src, file))


def extract_files(src:str, dst:str) -> None:
    env = UnityPy.load(src)
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            if obj.serialized_type.nodes:
                data = obj.read()
                tree = obj.read_typetree()
                fp = os.path.join(dst, f"{data.name}.json")
                with open(fp, "wt", encoding = "utf8") as f:
                    json.dump(tree, f, ensure_ascii = False, indent = 4)
            else:
                data = obj.read()
                fp = os.path.join(dst, f"{data.name}.bin")
                with open(fp, "wb") as f:
                    f.write(data.raw_data)
            print("[INFO  ]: done ", data.name)
            if obj.serialized_type.nodes:
                tree = obj.read_typetree()
                obj.save_typetree(tree)


if __name__ == "__main__":
    mdir: str|None = get_master_path()
    if mdir == None or mdir == "":
        print("[ERROR ]: Cannot find masters folder...")
        exit(1)

    src:str = "data/tmp/jp"
    dst:str = "data/JP"
    copy_files(src, mdir, dst)
    extract_files(src, dst)
    shutil.rmtree("data/tmp/jp")
