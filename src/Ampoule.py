
from globals import *

def header() -> str:
	return """{| class="wikitable sortable" style="width:100%; text-align: left;"
|+
!Character
!Title
!Evility
"""

def footer() -> str:
	return """|}
[[Category:Lists]]
"""

def ampoule_leaderskill(c:dict) -> str:
	aid = c["ampoule_leader_skill_number"]
	lid = c["m_leader_skill_id"]
	if aid > 0: lid = c[f"m_leader_skill_id_sub_{aid}"]
	return f"""{{{{JP/LeaderSkill/{lid}}}}}"""

def char_box(cid:int) -> str:
	return f"""{{{{CharacterNavFrameJP|{cid}}}}}"""

def add_character(char:dict, cid:int) -> str:
	return f"|-\n| {char_box(cid)}{ampoule_leaderskill(char)}\n"

def compose_webpage() -> str:
	webpage = header()
	for c in Charas:
		id = c["id"]
		if not is_chara_playable(c): continue
		if id >= 30000 and id % 4 != 1: continue
		webpage += add_character(c, c["id"])
	webpage += footer()
	return webpage


def main():
	RewritePage("Ampoule_Characters", compose_webpage())


if __name__ == "__main__":
	main()