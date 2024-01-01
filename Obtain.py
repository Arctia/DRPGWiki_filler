
from globals import *

string = f"<includeonly>{{{{#switch: {{{{{{1}}}}}}\n"

for c in Charas:
	if (c["id"]>10000 and c["id"] < 20000) or c["id"] > 49000 or c["m_leader_skill_id"] == 0:
		obt = "Unplayable"
	else:
		obt = "[[File:Premium Summon Banner.png|150px|link=Premium Summon]] (default value)"
	string += f"| {c['id']} = {obt}\n"

string += f"|}}}}</includeonly><noinclude>\n[[Category:Enum]][[Category:TranslationTables]] \n</noinclude>"

with open("./txt_files/obtain.txt", "w", encoding="utf-8") as f:
	f.write(string)