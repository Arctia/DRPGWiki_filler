
from globals import *

folder = "./Equipment/"

def Armors():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! DEF min !! Price !! Description
"""
	for w in Equipment:
		if w["equipment_type"] == 11:
			string += Armor(w)
	string += f"""|}}"""
	WriteFile(string, "Armor",)
	return string

def Armor(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["def_min"]}
|{w["price"]}
|{w["description"]}
"""

def Belts():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! HP min !! ATK min !! Price !! Description
"""
	for w in Equipment:
		if w["equipment_type"] == 12:
			string += Belt(w)
	string += f"""|}}"""
	WriteFile(string, "Belt",)
	return string

def Belt(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["hp_min"]}
|{w["atk_min"]}
|{w["price"]}
|{w["description"]}
"""

def Shoes():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! DEF min !! RES min !! SPD !! Price !! Description
"""
	for w in Equipment:
		if w["equipment_type"] == 13:
			string += Shoe(w)
	string += f"""|}}"""
	WriteFile(string, "Shoes",)
	return string

def Shoe(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["def_min"]}
|{w["res_min"]}
|{w["spd_min"]}
|{w["price"]}
|{w["description"]}
"""

def Orbs():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! INT min !! RES min !! Price !! Description
"""
	for w in Equipment:
		if w["equipment_type"] == 14:
			string += Orb(w)
	string += f"""|}}"""
	WriteFile(string, "Orb",)
	return string

def Orb(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["inte_min"]}
|{w["res_min"]}
|{w["price"]}
|{w["description"]}
"""

def Glassess():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! DEF min !! INT min !! RES min !! Price !! Description
"""
	for w in Equipment:
		if w["equipment_type"] == 15:
			string += Glasses(w)
	string += f"""|}}"""
	WriteFile(string, "Glasses",)
	return string

def Glasses(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["def_min"]}
|{w["inte_min"]}
|{w["res_min"]}
|{w["price"]}
|{w["description"]}
"""

def Muscles():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! HP min !! Price !! Description
"""
	for w in Equipment:
		if w["equipment_type"] == 16:
			string += Muscle(w)
	string += f"""|}}"""
	WriteFile(string, "Muscle",)
	return string

def Muscle(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["hp_min"]}
|{w["price"]}
|{w["description"]}
"""

def Treasures():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! HP min !! ATK/DEF/INT/RES !! SPD !! Price !! Description
"""
	for w in Equipment:
		if w["equipment_type"] == 17:
			string += Treasure(w)
	string += f"""|}}"""
	WriteFile(string, "Treasure",)
	return string

def Treasure(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["hp_min"]}
|{w["atk_min"]}
|{w["spd_min"]}
|{w["price"]}
|{w["description"]}
"""

def Rank(v):
	if v > 100 and v <200:
		return v - 100
	else:
		return v

def WriteFile(text, path):
	with open(folder+path, "w", encoding="utf-8") as file:
		file.write(text)
	print("Uploading %s" % path)
	page = wiki.pages[f"Equipments/{path}"]
	Upload(page, text)

def Main():
	Armors()
	Shoes()
	Belts()
	Muscles()
	Orbs()
	Glassess()
	Treasures()

Main()