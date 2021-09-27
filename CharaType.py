
import sys
import time
from globals import *

def _not_usable(c):
	if c["m_leader_skill_id"] == 0 or c["id"]>40000:
		return True
	return False

def _template(c, rarity):
	return f"""{{{{CharacterNavBoxFrame|{c["id"]}|Weapon={c["best_weapon_type"]}|kind={"human" if c['character_type'] == 1 else 'monster'}|JP=true|rarity={rarity}|type={EnumEvilSymbol[c["m_potential_class_id"]]}}}}}"""

def main():
	print("starting the work")
	string = ""
	
	types= {"kings": "", "pawns": "", "rooks": "",
			"queens": "", "knights": "", "bishops": ""}
	type_ids = [None, "kings", "pawns", "rooks", "bishops", "knights", "queens"]


	for _type in range(1,7):
		for c in Charas:
			if _not_usable(c): continue
			if _type == c["m_potential_class_id"] and c["unique_flg"] == 1:
				types[type_ids[_type]] += _template(c, rarity=5)

	for _type in range(1,7):
		types[type_ids[_type]] += "<br>"
		for c in Charas:
			if _not_usable(c): continue
			if _type == c["m_potential_class_id"] and c["unique_flg"] == 0:
				types[type_ids[_type]] += _template(c, rarity=4)

	for key in types:
		with open(f"./txt_files/{'jp_' if JP else''}{key}.txt", "w", encoding="utf-8") as f:
			f.write(types[key])
			page = wiki.pages[f"Template:Characters{'JP' if JP else ''}/{key}"]
			content = types[key] + f"\n[[Category:Lists]]"
			Upload(page, content, True)

main()