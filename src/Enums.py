
from globals import *

def _not_usable(c):
	if c["m_leader_skill_id"] == 0 or c["id"]>40000:
		return True
	return False

def main():

	PotentialClass = ""
	Gender = ""
	Kind = ""
	PreferiteWeapon = ""
	BaseRarity = ""

	for c in Charas:

		PotentialClass += f"""\n| {c['id']} = {c["m_potential_class_id"]}"""
		Gender += f"""\n| {c['id']} = {c["gender"]}"""
		Kind += f"""\n| {c['id']} = {c["character_type"]}"""
		PreferiteWeapon += f"""\n| {c['id']} = {c["best_weapon_type"]}"""
		BaseRarity += f"""\n| {c['id']} = {c["base_rare"]}"""

	start_fragment = f"""<includeonly>{{{{#switch: {{{{{{1}}}}}}"""
	end_fragment = f"""\n|}}}}</includeonly><noinclude>
[[Category:Enum]]
</noinclude>"""
	
	page = wiki.pages[f"Template:Enum/Chara/PotentialClass"]
	content = start_fragment + PotentialClass + end_fragment
	Upload(page, content, True)

	page = wiki.pages[f"Template:Enum/Chara/Gender"]
	content = start_fragment + Gender + end_fragment
	Upload(page, content, True)

	page = wiki.pages[f"Template:Enum/Chara/Kind"]
	content = start_fragment + Kind + end_fragment
	Upload(page, content, True)

	page = wiki.pages[f"Template:Enum/Chara/PreferiteWeapon"]
	content = start_fragment + PreferiteWeapon + end_fragment
	Upload(page, content, True)

	page = wiki.pages[f"Template:Enum/Chara/BaseRarity"]
	content = start_fragment + BaseRarity + end_fragment
	Upload(page, content, True)

main()