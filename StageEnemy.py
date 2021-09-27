
from globals import *

epath = "./datas/GL/MEnemy_"

e_number = 9
StageEnemies = []

for x in range(e_number):
	with open(epath + str(x+1) + ".json", encoding="utf-8") as file:
		StageEnemies += json.load(file)

def main():
	reached_id = 101102114
	switch = False

	for e in StageEnemies:
		if e["id"] == reached_id: switch = True
		if not switch: continue

		content = Enemy(e)
		page = wiki.pages[f"Template:Stage/Enemy/{e['id']}"]

		print(content) if not uploading else Upload(page, content)
		printl("Enemy id:   %s                    " % e["id"])

def WriteEnemies(sid, write=False):
	elist = []
	for e in StageEnemies:
		if sid != int(str(e["id"])[:-3]): continue
		elist.append(e["id"])
		page = wiki.pages[f"Template:Stage/Enemy/{e['id']}"]
		if not page.exists:
			content = Enemy(e)
			page = wiki.pages[f"Template:Stage/Enemy/{e['id']}"]
			print(content) if not uploading else Upload(page, content, False)
			printl("Enemy id:   %s                    " % e["id"])
	return elist

def Enemy(e):
	return f"""{{{{StageEnemyRaw
| spot = {Spot(e["id"])}
| id = {e["id"]}
| enemy_type = {e["enemy_type"]}
| m_character_id = {e["m_character_id"]}
| name = {e["name"]}
| serif = {e["serif"]}
| hp = {e["hp"]}
| atk = {e["atk"]}
| def = {e["def"]}
| inte = {e["inte"]}
| res = {e["res"]}
| spd = {e["spd"]}
| m_weapon_id = {e["m_weapon_id"]}
| m_command_id_1 = {e["m_command_id_1"]}
| command_lv_1 = {e["command_lv_1"]}
| m_command_id_2 = {e["m_command_id_2"]}
| command_lv_2 = {e["command_lv_2"]}
| m_command_id_3 = {e["m_command_id_3"]}
| command_lv_3 = {e["command_lv_3"]}
| m_command_id_4 = {e["m_command_id_4"]}
| command_lv_4 = {e["command_lv_4"]}
| overwrite_attr = {e["overwrite_attr"]}
| attr_fire = {e["attr_fire"]}
| attr_water = {e["attr_water"]}
| attr_wind = {e["attr_wind"]}
| attr_star = {e["attr_star"]}
| resist_poison = {e["resist_poison"]}
| resist_paralyze = {e["resist_paralyze"]}
| resist_sleep = {e["resist_sleep"]}
| resist_forget = {e["resist_forget"]}
| exp = {e["exp"]}
| drop_point_min = {e["drop_point_min"]}
| drop_point_max = {e["drop_point_max"]}
| regularly_turn_command = {e["regularly_turn_command"]}
| regularly_turn_command_turn = {e["regularly_turn_command_turn"]}
| timeline_position = {e["timeline_position"]}
{DList("drop_present_type", e)}
{DList("drop_present_id", e)}
{DList("drop_present_rarity", e)}
{DList("drop_present_num", e)}
{DList("drop_present_rate", e)}
{DList("command_rate_fine", e)}
{DList("command_rate_medium", e)}
{DList("command_rate_desperate", e)}
{DList("fixed_turn_command", e)}
{DList("fixed_turn_command_turn", e)}
}}}}"""

def Spot(i):
	s = int(str(i)[-1])
	t = ["", "A", "B", "C", "D", "E"]
	return t[s]

def DList(name, e):
	string = ""
	for i in range(6):
		string += f"""| {name}_{i+1} = """
		if i < e[name].__len__():
			string += str(e[name][i]) + "\n"
		else:
			string += "0\n"
	return string

if __name__ == "__main__":
	main()
