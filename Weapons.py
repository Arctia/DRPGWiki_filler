
from globals import *

folder = "./Weapons/"

def Swords():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! ATK min !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 1:
			string += Sword(w)
	string += f"""|}}"""
	WriteFile(string, "Sword",)
	return string

def Knuckles():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! ATK min !! SPD !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 2:
			string += Knuckle(w)
	string += f"""|}}"""
	WriteFile(string, "Knuckle")
	return string

def Spears():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! ATK min !! DEF min !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 3:
			string += Spear(w)
	string += f"""|}}"""
	WriteFile(string, "Spear")
	return string

def Bows():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! ATK min !! RES min !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 4:
			string += Bow(w)
	string += f"""|}}"""
	WriteFile(string, "Bow")
	return string

def Guns():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! ATK min !! SPD !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 5:
			string += Gun(w)
	string += f"""|}}"""
	WriteFile(string, "Gun")
	return string

def Axes():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! ATK min !! SPD !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 6:
			string += Axe(w)
	string += f"""|}}"""
	WriteFile(string, "Axe")
	return string

def Wands():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! INT min !! RES min !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 7:
			string += Wand(w)
	string += f"""|}}"""
	WriteFile(string, "Wand")
	return string

def Claws():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! ATK min !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 8:
			string += Claw(w)
	string += f"""|}}"""
	WriteFile(string, "Claw")
	return string

def Medals():
	string = f"""{{| class="wikitable sortable mw-collapsible" 
! !!Name !! Rank !! INT min !! RES min !! Price !! Description
"""
	for w in Weapons:
		if w["weapon_type"] == 9:
			string += Medal(w)
	string += f"""|}}"""
	WriteFile(string, "Medal")
	return string

def Sword(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["atk_min"]}
|{w["price"]}
|{w["description"]}
"""

def Knuckle(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["atk_min"]}
|{w["spd_min"]}
|{w["price"]}
|{w["description"]}
"""

def Spear(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["atk_min"]}
|{w["def_min"]}
|{w["price"]}
|{w["description"]}
"""

def Bow(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["atk_min"]}
|{w["res_min"]}
|{w["price"]}
|{w["description"]}
"""

def Gun(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["atk_min"]}
|{w["spd_min"]}
|{w["price"]}
|{w["description"]}
"""

def Axe(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["atk_min"]}
|'''{w["spd_min"]}'''
|{w["price"]}
|{w["description"]}
"""

def Wand(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["inte_min"]}
|{w["res_min"]}
|{w["price"]}
|{w["description"]}
"""

def Claw(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["atk_min"]}
|{w["price"]}
|{w["description"]}
"""

def Medal(w):
	return f"""|-
|[[File:equipment_icon-{w["icon_no"]}.png|50px|{w["name"]}]]
|{w["name"]}
|{Rank(w["item_rank"])}
|{w["inte_min"]}
|{w["res_min"]}
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
	page = wiki.pages[f"Weapons/{path}"]
	Upload(page, text)

def Main():
	Swords()
	Knuckles()
	Spears()
	Bows()
	Guns()
	Axes()
	Wands()
	Claws()
	Medals()

Main()