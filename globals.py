
import os, sys, getopt
import time
import json
import mwclient
import mtranslate
from user_data import username, password

# --- Setting default values
JP = True
uploading = False
CHARA_MODE = "new"
id_to_rewrite = []
reached_id = 1

EDIT = True
EDIT_SKILLS = True
PAGES_PATH = "./datas/text_pages/"
To_Edit = ["SkillsTable", "SpellsTable"]

# --- Getting terminal parameters
opts, args = getopt.getopt(sys.argv[1:],"hd:u:c:i:ri:",["data=", "upload=", "chara=", "ids=", "reachid="])
for opt, arg in opts:
	if opt in ("-d", "--data"):
		if arg == "gl":
			JP = False
	if opt in ("-u", "--upload"):
		if arg in ("y", "yes"):
			uploading = True
	if opt in ("-c", "--chara"):
		CHARA_MODE = arg
		if not arg in ("new", "edit", "rewrite", "n", "e", "r"):
			print("valid options for -c are [ new, edit, rewrite, n, e, r ]")
			sys.exit(2)
	if opt in ("-i", "--ids"):
		id_to_rewrite = [int(x) for x in arg.split(",")]
	if opt in ("-ri", "--reachid"):
		reached_id = int(arg)
	if opt in ("-h", "--help"):
		print("""	-c [--chara] <mode> \n	-i [--ids] <ids separated ,>
	-d [--data] <mode (gl, jp)>\n	-u [--upload] <y or n>
	-ri [--reachid] <id reached>""")
		sys.exit()

# --- Setting jp flag and log to the wikia
jp_flag = "JP/" if JP == True else ""
wiki = mwclient.Site('disgaea-rpg.fandom.com', path='/')
wiki.login(username=username, password=password)

#------------------------------------------------------
#	Load Game Dictionaries
#------------------------------------------------------

def _load_json_(_path):
	_flag = "JP" if JP else "GL"
	#_gl = "" if JP else "_1"
	_path = os.path.join(".", "datas", _flag, _path + ".json")
	with open(_path, encoding="utf-8") as f:
		_variable = json.load(f)["DataList"] if JP else json.load(f)
	return _variable

Charas, CharaCommands, CharaRetrofits, CharaMagicCommands, Commands, LeaderSkills, ClassNames, RitualTrainings, RebirthMaterials, Weapons, Equipment, CharacterStory, CharacterStoryTalk = [],[],[],[],[],[],[],[],[],[],[],[],[]
if JP:
	
	_e = {"character": Charas, "charactercommand": CharaCommands, "characterretrofit": CharaRetrofits, "charactermagiccommand": CharaMagicCommands, "command": Commands, "leaderskill": LeaderSkills, "characterclassname": ClassNames, "ritualtrainings": RitualTrainings, "necessaryrebirthmaterial": RebirthMaterials}
	for key in _e: _e[key] = _load_json_(key)
	Charas, CharaCommands, CharaRetrofits, CharaMagicCommands, Commands, LeaderSkills, ClassNames = _e["character"], _e["charactercommand"], _e["characterretrofit"], _e["charactermagiccommand"], _e["command"], _e["leaderskill"], _e["characterclassname"]
	RitualTrainings, RebirthMaterials =  _e["ritualtrainings"], _e["necessaryrebirthmaterial"]
else:
	_e = {"MCharacter_1": Charas, "MCharacterCommand_1": CharaCommands, "MCharacterRetrofit_1": CharaRetrofits, "MCharacterMagicCommand_1": CharaMagicCommands, "MCommand_1": Commands, "MLeaderSkill_1": LeaderSkills, "MCharacterClassName_1": ClassNames, "MWeapon_1": Weapons, "MEquipment_1": Equipment, "MCharacterStory_1": CharacterStory, "MCharacterStoryTalk_1": CharacterStoryTalk}
	for key in _e: _e[key] = _load_json_(key)
	Charas, CharaCommands, CharaRetrofits, CharaMagicCommands, Commands, LeaderSkills, ClassNames = _e["MCharacter_1"], _e["MCharacterCommand_1"], _e["MCharacterRetrofit_1"], _e["MCharacterMagicCommand_1"], _e["MCommand_1"], _e["MLeaderSkill_1"], _e["MCharacterClassName_1"],
	Weapons, Equipment, CharacterStory, CharacterStoryTalk = _e["MWeapon_1"], _e["MEquipment_1"], _e["MCharacterStory_1"], _e["MCharacterStoryTalk_1"]

#------------------------------------------------------
#	Methods
#------------------------------------------------------

def translate(value):
	try:
		if JP:
			return mtranslate.translate(value, "en", "auto")
		else:
			return value
	except:
		print("\ntranslation error, wait 30 secs to retry.")
		time.sleep(30)
		translate(value)

def Upload(page, content, edit=True):
	if page.exists and not edit: return
	if uploading:
		try:
			page.bot = True
			page.save(content, bot=True)
		except mwclient.errors.APIError:
			print("\nUploading failed retrying in 120 secs.")
			time.sleep(120)
			Upload(page, content)

def EditPage(page, text, reason='-'):
	try:
		page.edit(text, reason, bot=True)
	except mwclient.errors.APIError:
		print("\nEditing failed retrying in 120 secs.")
		time.sleep(120)
		EditPage(page, text, reason)

def printl(string, mode="[INFO	]: "):
	sys.stdout.flush()
	sys.stdout.write('\r' + mode + str(string)+'				')

#------------------------------------------------------
#	Some Usefull Enums
#------------------------------------------------------

SERIE = ["", "Disgaea 1", "Disgaea 2", "Disgaea 3", "Disgaea 4",
			 "Disgaea D2", "Disgaea 5", "Disgaea RPG", "Disgaea 6", 
			 "La Pucelle", "Makai Kingdom"]

EnumKind = {0: '', 1: 'Humanoid', 2: 'Monster'}

EnumEvilSymbol = {0: '', 
				  1: 'King', 
				  2: 'Pawn', 
				  3: 'Rook',
				  4: 'Bishop', 
				  5: 'Knight', 
				  6: 'Queen', }

EnumSerie = {0: "",
			 1: "Disgaea 1",
			 2: "Disgaea 2",
			 3: "Disgaea 3",
			 4: "Disgaea 4",
			 5: "Disgaea D2",
			 6: "Disgaea 5",
			 7: "Disgaea RPG",
			 8: "Disgaea 6",
			 9: "La Pucelle",
			 10: "Makai Kingdom",
			 }

EnumEventShops = {  301: "[[File:item icon-normal-301.png]]",
					2202: ""
					}

# --- Globals characters ID actually released because there are more in data
global_ids = [24, 95, 1, 2, 3, 4, 5, 6, 7, 8, 10, 21, 20002, 20003, 20020, 55, 54, 47, 20008, 44, 45, 20017, 16, 12, 20001, 42, 9, 11, 56, 48, 20021, 38, 20014, 18, 36, 21002, 49, 33, 1012, 1011, 20018, 13, 22, 59, 57, 58, 64, 15, 31, 63, 20022, 62, 37, 40, 20024, 20023, 43, 94, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10010, 10011, 10012, 10013, 10014, 10015, 10016, 10017, 10018, 10019, 10020, 10021, 10023, 10025, 10026, 10027, 10038, 10039, 30001, 30002, 30003, 30004, 20006, 30005, 30006, 30007, 30008, 30009, 30010, 30011, 30012, 30013, 30014, 30015, 30016, 30017, 30018, 30019, 30020, 30021, 30022, 30023, 30024, 30025, 30026, 30027, 30028, 30029, 30030, 30031, 30032, 30033, 30034, 30035, 30036, 30037, 30038, 30039, 30040, 30041, 30042, 30043, 30044, 30045, 30046, 30047, 30048, 30053, 30054, 30055, 30056, 30057, 30058, 30059, 30060, 30061, 30062, 30063, 30064, 21004, 30065, 30066, 30067, 30068, 30069, 30070, 30071, 30072, 30073, 30074, 30075, 30076, 30077, 30078, 30079, 30080, 30081, 30082, 30083, 30084, 30085, 30086, 30087, 30088, 30089, 30090, 30091, 30092, 30097, 30098, 30099, 30100, 30105, 30106, 30107, 30108, 30113,30114, 30115, 30116, 30117, 30118, 30119, 30120, 30125, 30126, 30127, 30128, 30129, 30130, 30131, 30132, 30133, 30134, 30135, 30136]
