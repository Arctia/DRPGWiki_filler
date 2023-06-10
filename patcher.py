
import UnityPy, shutil, json
from gst import *

src = os.path.join("datas", "JPTranslated")
src = "C:\\Users\\Arctia\\AppData\\LocalLow\\disgaearpg\\DisgaeaRPG\\assetbundle\\masters\\"
# src = os.path.join("output")
env = UnityPy.load(src)
path_M = os.path.join("datas", "JPMasters")

def copyfile(objname:str) -> bool:
	try:
		shutil.copy(objname, os.path.join(src, objname))
		return (True)
	except:
		print(f"[ERR   ]: {objname} cannot be copied to path {os.path.join(src, objname)}")
	return False

def load_unitypy_obj(objname:str):
	for obj in env.objects:
		if obj.type.name == "MonoBehaviour" and obj.serialized_type.nodes:
			if obj.read().name != objname: continue
			return (obj)
	return False

def save() -> None:
	env.save()
	print("[INFO  ]: environment saved.")

def empty_skils() -> dict:
	skill = {
		'id': 0,
		'name': None,
		'description_effect': None,
		'description': None
	}

def	empty_character() -> dict:
	chara = {
		'id': 0,
		'name': None,
		"class_name_1": None,
        "class_name_2": None,
        "class_name_3": None,
        "class_name_4": None,
        "class_name_5": None,
        "description": None,
	}
	return chara

def	replace_values(chara:dict, wc, col:int) -> None:
	chara['id'] = wc(RowIDS["Character ID"] + 1, col + 1).value
	chara['name'] = wc(RowIDS["Character Name"] + 1, col + 1).value
	for i in range(1, 6):
		chara[f'class_name_{i}'] = wc(RowIDS[f"Title {i + 1}"] + 1, col + 1).value
	chara['description'] = wc(RowIDS["Bio"] + 1, col + 1).value

worksheets = ['Unique Human', 'Unique Human 2', 'Unique Monster',
				'Human Generic', 'Monster Generic']

def patcher(characters:dict, skills:dict) -> None:
	for ws in worksheets:
		ws = workbook[ws]
		wc = ws.cell
		# select character column
		for col in range(2, ws.max_column + 1, 3):
			chara:dict = empty_character()
			replace_values(chara, wc, col)

			# select character in obj data
			for c in characters:
				if c['id'] == chara['id']: break
			
			# replace all character fields
			for key in chara:
				if key != 'id' and chara[key] != None: c[key] = chara[key]

			# replace all unique skills text
			sid:int = (300000 + c['id']) * 10
			for i in range(1, 5):
				for s in skills:
					if s['id'] == (sid + i):
						val:str = wc(RowIDS[f"Skill Name {i}"] + 1, col + 1).value
						if val != None: s['name'] = val
						val:str = wc(RowIDS[f"Skill Desc {i}"] + 1, col + 1).value
						if val != None: s['description'] = val
						val:str = wc(RowIDS[f"Skill Effect {i}"] + 1, col + 1).value
						if val != None: s['description_effect'] = val
			
			# replace all leaderskills


def main():
	obj_char = load_unitypy_obj("character")
	characters = obj_char.read_typetree()
	obj_skills = load_unitypy_obj("command")
	skills = obj_skills.read_typetree()

	# call the main patcher
	patcher(characters['DataList'], skills['DataList'])

	obj_char.save_typetree(characters)
	obj_skills.save_typetree(skills)
	save()

if __name__ == '__main__':
	main()
