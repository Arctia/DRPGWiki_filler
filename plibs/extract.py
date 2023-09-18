
import UnityPy, shutil, json, os
from config import Config

GAMEDATA_PATH = "C:\\Users\\Arctia\\AppData\\LocalLow\\disgaearpg\\DisgaeaRPG\\"
EXTRACT_PATH = "."

CHARA_FOLDER = "C:/Users/Arctia/AppData/LocalLow/disgaearpg/DisgaeaRPG/assetbundle/images/chara"
FRONT_FOLDER = "C:/Users/Arctia/AppData/LocalLow/disgaearpg/DisgaeaRPG/assetbundle/atlas/chara/battle/wait_front"

STOP_FOLDER = "images/chara_contest"

def	extract_data(src: str, dest: str, ids):
	for root, dirs, file in os.walk(src):
		for file_name in file:
			file_path = os.path.join(root, file_name)
			env = UnityPy.load(file_path)

			for path,obj in env.container.items():
				if obj.type.name in ["Texture2D", "Sprite"]:
					data = obj.read()
					paths = path.split("/")

					dst = os.path.join(dest, *path.split("/"))
					
					dst, ext = os.path.splitext(dst)
					fn = dst.split("\\")[-1].replace("front", "")

					switch = False
					for i in ids:
						if str(i) == fn or f"{str(i)}_1" == fn:
							switch = True
							if {str(i)}_1 == fn:
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
aids = jconf.get_aids()

# Delete old ones 
#if os.path.isdir(os.path.join(EXTRACT_PATH, "assets")):
#	shutil.rmtree(os.path.join(EXTRACT_PATH, "assets"))

print(ids)
# Extract new Images
extract_data(CHARA_FOLDER, EXTRACT_PATH, ids)
unpack_frames(FRONT_FOLDER, os.path.join(EXTRACT_PATH, "assets", "wait_front"), ids)

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
# jconf.__reset__()

