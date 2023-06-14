
import UnityPy, platform, shutil, json
from gst import *

src = "C:\\Users\\Arctia\\AppData\\LocalLow\\disgaearpg\\DisgaeaRPG\\assetbundle\\masters2\\"
if platform.system == 'Linux': src = os.path.join("datas", "JPMasters")

src = os.path.join("datas", "JPMasters")
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
	chara['id'] = wc(RowIDS["Character ID"] + 1, col).value
	chara['name'] = wc(RowIDS["Character Name"] + 1, col + 1).value
	for i in range(1, 6):
		chara[f'class_name_{i}'] = wc(RowIDS[f"Title {i + 1}"] + 1, col + 1).value
	chara['description'] = wc(RowIDS["Bio"] + 1, col + 1).value
	print(chara['name'])

worksheets = ['Unique Human', 'Unique Human 2', 'Unique Monster',
				'Human Generic', 'Monster Generic']

def patcher(characters:dict, skills:dict, leaderskills:dict) -> None:
	for ws in worksheets:
		ws = workbook[ws]
		wc = ws.cell
		# select character column
		for col in range(2, ws.max_column + 1, 3):
			chara:dict = empty_character()
			replace_values(chara, wc, col)

			# select character in obj data
			print(f"[START ]: character <{chara['id']}>")
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
			ll = [c['m_leader_skill_id'], c['m_leader_skill_id_sub_1'], c['m_leader_skill_id_sub_2'], c['m_leader_skill_id_sub_3']]
			al = [c['additional_m_leader_skill_id'], c['additional_m_leader_skill_id_sub_1'], c['additional_m_leader_skill_id_sub_2'], c['additional_m_leader_skill_id_sub_3']]
			for i in range(0, 4):
				lid:int = ll[i]
				alid:int = al[i]
				for l in leaderskills:
					if l['id'] != lid: continue

					name:str = wc(RowIDS[f"Evility Name {i + 1}"] + 1, col + 1).value
					if name != None: l['name'] = name
					effect:str = wc(RowIDS[f"Evility Desc {i + 1}"] + 1, col + 1).value
					if effect == None: continue

					# split if double leaderskill
					if alid != 0:
						if "," in effect:
							splitted = effect.rsplit(",", 1)
						elif "#PER2#" in effect:
							splitted = effect.rsplit("#PER2#", 1)
							splitted[1] = f"#PER2#{splitted[1]}"
						elif "and" in effect:
							splitted = effect.rsplit("and", 1)
						elif "&" in effect:
							splitted = effect.rsplit("&", 1)
						else:
							continue

						l['description'] = splitted[0]
						for l in leaderskills:
							if l['id'] != lid: continue
							l['description'] = splitted[1].replace("PER2", "PER")
							break
					else:
						l['description'] = effect
					break

			print(f"[DONE  ]: character <{c['id']}>")

def story_patcher(dialogues) -> None:

	stc_id 	= 10
	manual 	= 6
	google 	= 4

	wb = openpyxl.load_workbook('translation_sheet/story.xlsx')
	for ws in wb:
		wc = ws.cell
		for row in range(2, ws.max_row):
			_id_ = wc(row, stc_id).value
			if _id_ == None: continue
			message = wc(row, manual).value
			if message == None:	message = wc(row, google).value
			if message == None: continue
			for d in dialogues:
				if d['id'] == int(_id_):
					d['talk_text'] = message
					print(f"[WROTE   ]: {message}")
					break

def main():
	obj_char 	= load_unitypy_obj("character")
	characters 	= obj_char.read_typetree()
	obj_skills 	= load_unitypy_obj("command")
	skills 		= obj_skills.read_typetree()
	obj_lskills 	= load_unitypy_obj("leaderskill")
	lskills 		= obj_lskills.read_typetree()
	obj_stories	= load_unitypy_obj("storytalk")
	dialogues 	= obj_stories.read_typetree()

	# call the main patcher
	patcher(characters['DataList'], skills['DataList'], lskills['DataList'])
	story_patcher(dialogues['DataList'])

	obj_char.save_typetree(characters)
	obj_skills.save_typetree(skills)
	obj_lskills.save_typetree(lskills)
	obj_stories.save_typetree(dialogues)
	save()

if __name__ == '__main__':
	main()
