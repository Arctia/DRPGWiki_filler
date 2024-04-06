
import UnityPy, dotenv, os
from config import Config

# ----------------------------------------------------------------------#
# --- Load paths

dotenv.load_dotenv("../.env")

EXTRACT_PATH = "."
D_GAMEDATA = os.getenv("DRPGMasters_path")
if os.getenv("DRPG_DEFAULT_PATH") == "true":
    try:
        D_GAMEDATA = f"{os.getenv('LOCALAPPDATA')}\\..\\LocalLow\\disgaearpg\\DisgaeaRPG"
    except Exception as e:
        print(f"[ERROR ]: Failed to find master folder -> {e}")

D_CHAR = os.path.join(D_GAMEDATA, "assetbundle", "images", "chara")
D_FRONT = os.path.join(D_GAMEDATA, "assetbundle", "atlas", "chara", "battle", "wait_front")


# ----------------------------------------------------------------------#
# --- Extract Functions

def	extract_data(src: str, dest: str, ids):
	for root, dirs, file in os.walk(src):
		for file_name in file:
			file_path = os.path.join(root, file_name)
			env = UnityPy.load(file_path)

			for path,obj in env.container.items():
				if obj.type.name in ["Texture2D", "Sprite"]:
					data = obj.read()
					# paths = path.split("/")

					dst = os.path.join(dest, *path.split("/"))
					
					dst, ext = os.path.splitext(dst)
					fn = dst.split("\\")[-1].replace("front", "")

					switch = False
					for i in ids:
						if str(i) == fn.split("/")[-1] or f"{str(i)}_1" == fn.split("/")[-1]:
							switch = True
							if f"{str(i)}_1" == fn.split("/")[-1]:
								jconf.add_ex_char(i)
							break
					if not switch: continue

					os.makedirs(os.path.dirname(dst), exist_ok=True)
					dst += ".png"
					data.image.save(dst)
					print(f"[INFO  ]: Written: {dst}")

def unpack_frames(source_folder : str, destination_folder : str, ids):
	for root, dirs, files in os.walk(source_folder):
		for file_name in files:

			switch = False
			for i in ids:
				if str(i) == file_name.replace("front", ""):
					switch = True
					break
			if not switch: continue

			file_path = os.path.join(root, file_name)
			env = UnityPy.load(file_path)

			for obj in env.objects:
				if obj.type.name in ["Sprite"]:
					data = obj.read()
					dest = os.path.join(destination_folder, file_name, data.name)
					os.makedirs(os.path.dirname(dest), exist_ok = True)
					dest, ext = os.path.splitext(dest)
					dest = dest + ".png"
					img = data.image
					img.save(dest)

################################################ Main script
jconf = Config()
ids = jconf.get_ids()
mids = jconf.get_mids()
aids = jconf.get_aids()

# Delete old ones 
#if os.path.isdir(os.path.join(EXTRACT_PATH, "assets")):
#	shutil.rmtree(os.path.join(EXTRACT_PATH, "assets"))

if ids != None and ids != []:
	print(f"new chars: {ids}")
if mids != None and mids != []:
	print(f"mod chars: {mids}")

# Extract new Images
extract_data(D_CHAR, EXTRACT_PATH, ids)
unpack_frames(D_FRONT, os.path.join(EXTRACT_PATH, "assets", "wait_front"), ids)

ex_frames = jconf.get_exids()
ex_frames_1 = []
for id in ex_frames:
	if id in ids:
		ex_frames_1.append(f"{str(id)}_1")
unpack_frames(D_FRONT, os.path.join(EXTRACT_PATH, "assets", "wait_front"), ex_frames_1)

with open(os.path.join("..", "update_characters.sh"), "r") as f:
	lines = f.readlines()

for i in range(len(lines)):
	if "Character.py" in lines[i]:
		aids = [str(l) for l in aids]
		id_to_write = ",".join(aids)
		lines[i] = f"python3 Character.py -u y -d j -i {id_to_write} -c r\n"

with open(os.path.join("..", "update_characters.sh"), "w") as f:
	for l in lines:
		f.write(l)

# Reset chara configs after the work went fine
# jconf.__reset__()

