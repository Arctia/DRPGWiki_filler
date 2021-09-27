
import sys
import time
from globals import *

# * Rewrite using date for order

def main():
	print("starting the work\n")
	start = """All character stats are taken as if the unit has 4★, so a 2/3★ character can be compared with a 4★. 

Also note that for generics, only the first color is included, since their stats doesn't change while their evilities do so.
{| class="wikitable sortable" style="width:100%; text-align: center;"
|+
! 
!Name
!HP
!ATK
!DEF
!INT
!RES
!SPD """
	rows = ""
	name = ""
	for c in Charas:
		if c["m_leader_skill_id"] == 0 or c["id"]>40000: continue

		if name != c["name"]:
			if JP:
				rows += Add_Character(c)
			else:
				if c["id"] in global_ids: rows += Add_Character(c)

			name = c["name"]
			sys.stdout.write('\rCharacter %s' % str(c["id"]))
			sys.stdout.flush()

	with open(f"./txt_files/{'jp_' if JP else ''}table.txt", "w", encoding="utf-8") as f:
		f.write(start+ rows + f"\n|}}\n[[Category:Lists]]")
		if JP: page = wiki.pages["Japan_Characters_Stats_Comparison"]
		else: page = wiki.pages["Global_Characters_Stats_Comparison"]
		content = start+ rows + f"\n|}}\n[[Category:Lists]]"
		Upload(page, content, True)

def Add_Character(c):
	return f"""
|-
| {{{{CharacterNavBox{'JP' if JP else ''}|{c["id"]}|{c["name"]}|imgsize=64px}}}}
| [[{jp_flag}Character/{c["id"]}|{{{{Enum/JP/CharaName|{c["id"]}}}}}]]
| {c["hp_min"]}
| {c["atk_min"]}
| {c["def_min"]}
| {c["inte_min"]}
| {c["res_min"]}
| {c["spd_min"]}"""

main()