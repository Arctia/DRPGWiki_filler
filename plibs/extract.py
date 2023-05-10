
import UnityPy, shutil, json, os
from config import Config

GAMEDATA_PATH = "./folder"
EXTRACT_PATH = "."

FOLDERS_TO_CHECK = ['chara', "wait_front"]

def	extract_data(src: str, dest: str, ids):
	for root, dirs, file in os.walk(src):
		for file_name in file:
			file_path = os.path.join(root, file_name)
			env = UnityPy.load(file_path)

			for path,obj in env.container.items():
				if obj.type.name in ["Texture2D", "Sprite"]:
					data = obj.read()
					paths = path.split("/")
					switch = False
					
					# check if path is eligible of extraction
					for fd in FOLDERS_TO_CHECK:
						if fd in paths:
							switch = True
							break
					if not switch: continue
					

					dst = os.path.join(dest, *path.split("/"))
					os.makedirs(os.path.dirname(dst), exist_ok=True)
					dst, ext = os.path.splitext(dst)
					fn = dst.split("/")[-1].replace("front", "")

					switch = False
					for i in ids:
						if str(i) == fn:
							switch = True
							break
					if not switch: continue
					
					dst += ".png"
					data.image.save(dst)
					print(f"[INFO  ]: Written: {dst}")

################################################ Main script
jconf = Config()
ids = jconf.get_ids()
aids = jconf.get_aids()

# Delete old ones 
if os.path.isdir(os.path.join(EXTRACT_PATH, "assets")):
	shutil.rmtree(os.path.join(EXTRACT_PATH, "assets"))

# Extract new Images
extract_data(GAMEDATA_PATH, EXTRACT_PATH, ids)

with open(os.path.join("..", "update_characters.sh"), "r") as f:
	lines = f.readlines()

for i in range(len(lines)):
	if "Character.py" in lines[i]:
		aids = [str(l) for l in aids]
		id_to_write = ",".join(aids)
		lines[i] = f"py Character.py -u y -d j -i {id_to_write} -c r\n"

with open(os.path.join("..", "update_characters.sh"), "w") as f:
	for l in lines:
		f.write(l)

# Reset chara configs after the work went fine
jconf.__reset__()

