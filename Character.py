
import time
import InfoBox
from globals import *
import Skills
import LeaderSkills

edit_ids = [1]

def main():
	switch = False
	for c in Charas:
		if c["id"] == reached_id: switch = True
		if not switch: continue

		if CHARA_MODE in ("new", "n"): New_Characters(c)
		elif CHARA_MODE in ("edit", "e"):
			if c["id"] < 40000 and c["m_leader_skill_id"] != 0 and c["id"] > 0:
				Edit_Characters(c)
		elif CHARA_MODE in ("rewrite", "r"):
			if c["id"] in id_to_rewrite: Rewrite_Characters(c, False)
		elif CHARA_MODE in ("rewrite-all", "rall"):
			Rewrite_Characters(c, False)


def Rewrite_Characters(c, skip_templates=False):
	print(f"\nStarted uploading character id: {c['id']}")
	if not skip_templates:
		for part in DD:
			if not JP and part[1] == "RitualTraining": continue
			content = part[1](c)
			page = wiki.pages[f'Template:{jp_flag}Character/{c["id"]}/{part[0]}']
			print(content) if not uploading else Upload(page, content, True)
			printl(f"""Done {c["id"]} {part[0]}""")

	content = MainTemplate(c)
	page = wiki.pages[f'{jp_flag}Character/{c["id"]}']
	if "#REDIRECT" in page.text():
		uri = page.text().split("[[")[1].split("]]")[0]
		page = wiki.pages[f'{uri}']
	print(content) if not uploading else Upload(page, content)

	printl(f"Uploaded character id: {c['id']}\n")

def New_Characters(c):
	page = wiki.pages[f'{jp_flag}Character/{c["id"]}']
	if page.exists: 
		print(f"Passing character id: {c['id']}")
		return
	Rewrite_Characters(c)

def Edit_Characters(c):
	print(f"\nStarted Editing character id: {c['id']}")
	for part in DD:
		if not part[0] in To_Edit: continue
		content = part[1](c)
		page = wiki.pages[f'Template:{jp_flag}Character/{c["id"]}/{part[0]}']
		print(content) if not uploading else Upload(page, content, EDIT)
		printl(f"""Done {c["id"]} {part[0]}			""")

	Edit_Main_Template(c)

	printl(f"Edited character id: {c['id']}\n")

def Edit_Main_Template(c):
	page = wiki.pages[f'{jp_flag}Character/{c["id"]}']
	try:
		content = page.text()
		tt = content
	except:
		time.sleep(120)
		Edit_Main_Template(c)
		return

	if "#REDIRECT" in content:
		uri = content.split("[[")[1].split("]]")[0]
		page = wiki.pages[f'{uri}']

	try:
		content = page.text()
		tt = content
	except:
		time.sleep(120)
		Edit_Main_Template(c)
		return

	if "Category" in To_Edit:
		text = content
		categories = GetCategories(c)
		v = 0
		for cat in categories:
			if not cat in text:
				text += cat
				v += 1
		if v > 0: 
			#EditPage(text, 'Categories Fix')
			content = text

	if "AddRitualTraining" in To_Edit:
		text = content
		### Add before Navigation
		to_put = f"""{Rituals(c)}\n\n==Gallery=="""
		text = text.replace("==Gallery==", to_put)
		content = text
	
	if tt != content:
		print(content) if not uploading else EditPage(page, content, '')

def GetCategories(c):
	array = []
	array2 = []
	array.append(EnumKind[int(c["character_type"])])
	for si in c["series_ids"]:
		array.append(EnumSerie[int(si)])
	if JP:
		array.append(EnumEvilSymbol[c["m_potential_class_id"]])
	for e in array:
		if e != "":
			array2.append('[[Category:'+ jp_flag + e + ']]')

	return array2


def MainTemplate(c):
	return f"""{{{{DISPLAYTITLE:{{{{Enum/JP/CharaName|{c["id"]}}}}} }}}}
{{{{{jp_flag}Character/{c["id"]}/InfoBox}}}}
{{{{{jp_flag}Character/{c["id"]}/Description}}}}
{Playable(c)}
==Character Links==
{{{{{jp_flag}Character/{c["id"]}/CharacterLinks}}}}

==Gallery==
{Gallery(c)}
{Gallery2(c)}

===Navigation===
[[JP/Characters|To Character List]]

<noinclude>
[[Category:{jp_flag}Character]]
[[Category:{f"{jp_flag}Unique" if c['unique_flg'] else f"{jp_flag}Generic"}]]
[[Category:{f"{jp_flag}Humanoid" if c['character_type'] == 1 else f"{jp_flag}Monster"}]]
{Categories(c)}
</noinclude>
"""

def Playable(c):
	if c["m_leader_skill_id"] != 0 and c["id"] < 40000:
		return f"""
==Statistics==

===Stats===
{{{{{jp_flag}Character/{c["id"]}/StatsTable}}}}

===Attributes===
{{{{{jp_flag}Character/{c["id"]}/AttrTable}}}}

===Resistances===
{{{{{jp_flag}Character/{c["id"]}/ResTable}}}}

===Weapon Mastery===
{{{{{jp_flag}Character/{c["id"]}/WeaponMasteryTable}}}}

==Commands==

===Evilities===
{{{{{jp_flag}Character/{c["id"]}/LeaderSkillsTable}}}}

===Skills===
{{{{{jp_flag}Character/{c["id"]}/SkillsTable}}}}

===Magic Spells===
{{{{{jp_flag}Character/{c["id"]}/SpellsTable}}}}

===Nether Enhancement===
{{{{{jp_flag}Character/{c["id"]}/NetherEnhancementTable}}}}
{Rituals(c)}
"""
	else:
		return f"""=='''UNPLAYABLE'''==
<br>
<br>
<br>
"""

#################################################################################################
#------------- Sub Categories
#################################################################################################

def Description(c):
	if JP:
		return f"{{{{Enum/JP/Bios|{c['id']}}}}}" #translate(c["description"])
	else:
		return f"{c['description']}"

def StatsTable(c):
	return f"""{{{{StatsTableRaw
|hp_min      = {c["hp_min"]}
|hp_per_lv   = {c["hp_per_lv"]}
|atk_min     = {c["atk_min"]}
|atk_per_lv  = {c["atk_per_lv"]}
|def_min     = {c["def_min"]}
|def_per_lv  = {c["def_per_lv"]}
|inte_min    = {c["inte_min"]}
|inte_per_lv = {c["inte_per_lv"]}
|res_min     = {c["res_min"]}
|res_per_lv  = {c["res_per_lv"]}
|spd_min     = {c["spd_min"]}
|spd_per_lv  = {c["spd_per_lv"]}
|base_rare = {c["base_rare"]}
}}}}"""

def AttrTable(c):
	return f"""{{{{AttributeTable
|Fire  = {c["attr_fire"]}
|Water = {c["attr_water"]}
|Wind  = {c["attr_wind"]}
|Star  = {c["attr_star"]}
}}}}"""

def ResTable(c):
	return f"""{{{{ResistanceTable
|Poison   = {c["resist_poison"]}
|Paralyze = {c["resist_paralyze"]}
|Sleep    = {c["resist_sleep"]}
|Forget   = {c["resist_forget"]}
}}}}"""

def WeaponMasteryTable(c):
	return f"""{{{{WeaponMasteryTable
|Sword   = {c["weapon_mastery_rank_1"]}
|Knuckle = {c["weapon_mastery_rank_2"]}
|Spear   = {c["weapon_mastery_rank_3"]}
|Bow     = {c["weapon_mastery_rank_4"]}
|Gun     = {c["weapon_mastery_rank_5"]}
|Axe     = {c["weapon_mastery_rank_6"]}
|Wand    = {c["weapon_mastery_rank_7"]}
|Claw    = {c["weapon_mastery_rank_8"]}
|Medal   = {c["weapon_mastery_rank_9"]}
|Pref    = {c["best_weapon_type"]}
}}}}"""

def CharacterLinks(c):
	string = f"{{{{{jp_flag}CharacterLinksRaw\n"
	count = 1
	for link in c["linkage_character_ids"]:
		string += f"""| linkage_character_ids_{count} = {link}\n"""
		count += 1
	string += f"}}}}"
	return string

def LeaderSkillsTable(c):
	cl = LeaderSkills.create_leader_skill
	cl(c["m_leader_skill_id"], EDIT)
	cl(c["m_leader_skill_id_sub_1"], EDIT)
	cl(c["m_leader_skill_id_sub_2"], EDIT)
	cl(c["m_leader_skill_id_sub_3"], EDIT)
	return f"""{{{{{jp_flag}LeaderSkillsTableRaw
| id = {c["id"]}
| m_leader_skill_id = {c["m_leader_skill_id"]} 
| m_leader_skill_id_sub_1 = {c["m_leader_skill_id_sub_1"]}
| m_leader_skill_id_sub_2 = {c["m_leader_skill_id_sub_2"]} 
| m_leader_skill_id_sub_3 = {c["m_leader_skill_id_sub_3"]} 
| ampoule_skill = {c["ampoule_leader_skill_number"]}
}}}}"""

#################################################################################################
#------------- Sub Categories - Spells and Skills
#################################################################################################

def SkillsTable(c):
	skills_id = []
	for cc in CharaCommands:
		if cc["m_character_id"] == c["id"]:
			skills_id.append([cc["m_command_id"], cc["lv"]])
	for cr in CharaRetrofits:
		if cr["m_character_id"] == c["id"]:
			if cr["retrofit_type"] == 1:
				skills_id.append([cr["retrofit_value"], "N. E. +3"])

	for skill in skills_id: Skills.create_skill(skill[0], EDIT_SKILLS, True)

	string = f"{{{{{jp_flag}SkillsTableRaw\n"
	count = 1
	for skill in skills_id:
		string += f"""|skill_id_{count} = {str(skill[0])}\n|skill_lv_{count} = {str(skill[1])}\n"""
		count += 1
	string += f"}}}}"
	return string

def SpellsTable(c):
	spells_id = []
	for mc in CharaMagicCommands:
		if mc["m_character_id"] == c["id"]:
			spells_id.append([mc["m_command_id"], mc["weapon_mastery_lv"]])

	# Create Spells but they're already there
	#for spell in spells_id: Skills.create_skill(spell[0], EDIT)

	string = f"{{{{Template:{jp_flag}SpellsTableRaw\n"
	count = 1
	for spell in spells_id:
		string += f"|spell_id_{count} = {str(spell[0])}\n|spell_wm_{count} = {str(spell[1])}\n"
		count += 1
	string += f"}}}}"
	return string

def NetherEnhancementTable(c):
	arr = RetroFitsTable(c)
	string = ""
	if arr[1] == 16: string = "15"
	elif arr[1] == 21: string = "20"
	return f"""{{{{NetherEnhancementTable{string}Raw
{arr[0]}
}}}}"""

def RetroFitsTable(c):
	string = f""
	count = 1
	for r in CharaRetrofits:
		if r["m_character_id"] == c["id"]:
			if r["retrofit_type"] == 1: string += f"""| row_{count} = Unlock Skill: '''{{{{Enum/JP/Skills|{r["retrofit_value"]}}}}}'''"""
			elif r["retrofit_type"] == 3: string += f"""| row_{count} = Parameters '''+{r["retrofit_value"]}%'''"""
			elif r["retrofit_type"] == 2: string += f"""| row_{count} = Unlock Evility: '''{{{{Enum/JP/LeaderSkills|{c["id"]}{int(r["retrofit_value"])+1}}}}}'''"""
			elif r["retrofit_type"] == 4: string += f"""| row_{count} = Unique Skills SP Consumption '''-{r["retrofit_value"]}'''"""
			elif r["retrofit_type"] == 6: string += f"""| row_{count} = ATK '''+{r["retrofit_value"]}%'''"""
			elif r["retrofit_type"] == 8: string += f"""| row_{count} = INT '''+{r["retrofit_value"]}%'''"""
			elif r["retrofit_type"] == 14: string += f"""| row_{count} = HP / DEF / RES '''+{r["retrofit_value"]}%'''"""
			elif r["retrofit_type"] == 10: string += f"""| row_{count} = Flame Resistance '''+{r["retrofit_value"]}%'''"""
			elif r["retrofit_type"] == 11: string += f"""| row_{count} = Water Resistance '''+{r["retrofit_value"]}%'''"""
			elif r["retrofit_type"] == 12: string += f"""| row_{count} = Wind Resistance '''+{r["retrofit_value"]}%'''"""
			elif r["retrofit_type"] == 13: string += f"""| row_{count} = Star Resistance '''+{r["retrofit_value"]}%'''"""
			string += f"\n"
			count += 1
	return [string, count]

def Rituals(c, tabber=False):
	if JP and tabber:
		return f"""|-| Killia's Training = {{{{{jp_flag}Character/{c["id"]}/RitualTraining}}}}"""
	elif JP:
		return f"""\n===Killia's Training===\n{{{{{jp_flag}Character/{c["id"]}/RitualTraining}}}}"""
	else:
		return f""

def RitualTrainingTable(c):
	return f"""{{{{RitualTrainingTableRaw
{RitualTrainingRows(c)}
}}}}"""

def RitualTrainingRows(c):
	string = f""
	count = 1
	if JP:
		for r in RitualTrainings:
			if r["m_character_id"] == c["id"]:
				if r["training_type"] == 1:
					try:
						s = r["ability_description"].split("[")[1].split("]")[0]
						string += f"""| row_{count} = '''{{{{Enum/JP/Skills|{r["ability_id"]}}}}}''' [{translate(s)}]"""
					except:
						string += f"""| row_{count} = {translate(r["ability_description"])}"""
				elif count == 10: 
					string += f"""| row_{count} = {translate(r["ability_description"])}"""
				else: 
					string += f"""| row_{count} = {r["ability_description"]}"""
				string += f"\n"
				count += 1
		return string

#################################################################################################
#------------- Subs in Main Template
#################################################################################################

def Gallery(c):
	return f"""{{{{#tag:gallery|
Chara-illust-{c["id"]}.png{{{{!}}}}Illustration
Chara-face-{c["id"]}.png{{{{!}}}}Portrait
Chara-command-{c["id"]}.png{{{{!}}}}Command
Chara-ci-{c["id"]}.png{{{{!}}}}CutIn
|type=slideshow |position=center |widths=500}}}}"""

def Gallery2(c):
	if not c["id"] in cf.get_exids(): return ""
	return f"""
==EX Gallery==
{{{{#tag:gallery|
Chara-illust-{c["id"]}_1.png{{{{!}}}}Illustration
Chara-face-{c["id"]}_1.png{{{{!}}}}Portrait
Chara-command-{c["id"]}_1.png{{{{!}}}}Command
Chara-ci-{c["id"]}_1.png{{{{!}}}}CutIn
|type=slideshow |position=center |widths=500}}}}"""

def Categories(c):
	string = ""
	for serie_id in c["series_ids"]:
		if SERIE[serie_id] != "":
			string += f"""[[Category:{jp_flag}{SERIE[serie_id]}]]\n"""
	if JP:
		Symbol = ["", "King", "Pawn", "Rook", "Bishop", "Knight", "Queen"]
		string += f"""[[Category:{jp_flag}{Symbol[c["m_potential_class_id"]]}]]\n"""
	if c['id'] in cf.get_exids():
		string += f"""[[Category:EX]]\n"""
	return string

def Navigation(c):
	# return f"""..."""
	return f"""{{{{{jp_flag}Characters}}}}"""

DD = [["InfoBox", InfoBox.create_page], ["Description", Description], ["StatsTable", StatsTable],
		 ["AttrTable", AttrTable], ["ResTable", ResTable], ["WeaponMasteryTable", WeaponMasteryTable],
		 ["CharacterLinks", CharacterLinks], ["LeaderSkillsTable", LeaderSkillsTable],
		 ["SkillsTable", SkillsTable], ["SpellsTable", SpellsTable], ["NetherEnhancementTable", NetherEnhancementTable],
		 ["RitualTraining", RitualTrainingTable], ]

if __name__ == "__main__":
	main()
