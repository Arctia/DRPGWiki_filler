
from globals import *

reb_type = 2

content = f"""<div class="tabbertab-borderless"><tabber>
"""
counter = 1

reinc_number_mat = {}
maximum_hl = 0

def calc_maximum(r, id):
	if r[f"m_item_id_{id}"] in reinc_number_mat:
		reinc_number_mat[r[f"m_item_id_{id}"]] += r[f"necessary_num_{id}"]
	else:
		reinc_number_mat[r[f"m_item_id_{id}"]] = r[f"necessary_num_{id}"]

def prefix(c):
	values = [1,11,21,31,41,51,61,71,81,91]
	if c in values:
		if reb_type == 1:
			return f"""|-|Lv {c*100}-{(c+9)*100}= {{| class="wikitable" style="width:100%; text-align:center;"
! Lv !! Mat 1 !! Mat 2 !! Mat 3 !! Mat 4 !! Mat 5 !! Mat 6 !! Mat 7 !! HL\n"""
		else:
			return f"""|-|Lv {c*100}-{(c+9)*100}= {{| class="wikitable" style="width:100%; text-align:center;"
! Lv !! Mat 1 !! Mat 2 !! Mat 3 !! Mat 4 !! Mat 5 !! Mat 6 !! Mat 7 !! HL\n"""
	return f""

def requirement(r, id):
	if r[f"m_item_id_{id}"] != 0:
		calc_maximum(r, id)
		return f"""[[File:item_icon_{r[f"m_item_id_{id}"]}.png|50px]] x{r[f"necessary_num_{id}"]}"""
	else:
		return ""

for r in RebirthMaterials:
	if r["rebirth_type"] == reb_type:
		content += prefix(counter)
		content += f"""
|-
|{r["rebirth_num"]*100}
|{requirement(r, "1")}
|{requirement(r, "2")}
|{requirement(r, "3")}
|{requirement(r, "4")}
|{requirement(r, "5")}
|{requirement(r, "6")}
|{requirement(r, "7")}
|{r["necessary_hl_num"]}"""
		maximum_hl += r["necessary_hl_num"]
		if counter in [10,20,30,40,50,60,70,80,90,99]:
			content += f"""\n|}}\n"""
		counter += 1

def write_maximum_materials():
	string = f""
	for key in reinc_number_mat:
		string += f"""
|-
|[[File:item_icon_{key}.png|50px]]
| x {reinc_number_mat[key]}"""
	return string

content += f"""\n</tabber></div>

{{| class="wikitable" style="text-align:center;"
{write_maximum_materials()}
|-
|HL
|{maximum_hl}
|}}
"""

with open(PAGES_PATH + "reinc.txt", "w", encoding="utf-8") as f:
	f.write(content)

print(reinc_number_mat)
