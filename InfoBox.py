
from globals import *

def create_page(c):
	return f"""{{{{{jp_flag}CharacterInfoBoxRaw
|id = {c["id"]}
|name  = {translate(c["name"])}
|image1  = Chara-illust-{c["id"]}.png
|gender  = {{{{Template:Enum/Gender|{c["gender"]}}}}}
|type = {Type(c)}
|series  = {Series(c)}
|cv      = {translate(c["cv_name"])}
|sell_point    = {c["sell_point"]}
|sell_soul = {Soul(c)}
{Classes(c)}
|base_rare = {c["base_rare"]}
}}}}"""

def Type(c):
	#if JP:
	return f"""{{{{Template:Enum/Kind|{c["character_type"]}}}}}[[File:Equipment_icon-{c["best_weapon_type"]}.png]]{{{{#ifexpr: {c["m_potential_class_id"]} = 0| | {{{{Enum/EvilSymbol|{c["m_potential_class_id"]}}}}}}}}}"""
	#else:
	#return f"""{{{{Template:Enum/Kind|{c["character_type"]}}}}}[[File:Equipment_icon-{c["best_weapon_type"]}.png]]"""

def Series(c):
	string = f""
	for serie in c["series_ids"]:
		string += f"""{{{{Template:Enum/Series|{serie}}}}}"""
	return string

def Classes(c):
	cn = []
	for cc in ClassNames:
		if cc["m_character_id"] == c["id"]:
			cn.append(cc["class_name"])

	string = ""

	for cl in range(6):
		string += f"""|class_name_{cl} = {{{{#ifexpr: {c["base_rare"]}<{cl+2} | """
		string += f"""{{{{Enum/JP/Titles|{c['id']}{cl+1}}}}}"""
		string += f""" | }}}}\n"""
	return string

def Soul(c):
	if JP:
		return f"""{c["sell_soul"]}"""
	else:
		return f""

def edit():
	print("begin to modify")
	for c in Charas:
		page = wiki.pages[f"Template:{jp_flag}Character/{c['id']}/InfoBox"]
		text = page.text()
		content = text.replace("{{CharacterInfoBoxRaw", "{{JP/CharacterInfoBoxRaw")
		if content != text:
			print(content) if not uploading else EditPage(page, content, 'Adding JP Infobox for How to obtain')
			printl("character id: %s" % int(c['id']))

def rewrite_type():
	print("begin to modify")
	for c in Charas:
		if not c["id"] in global_ids: continue
		page = wiki.pages[f"Template:{jp_flag}Character/{c['id']}/InfoBox"]
		text = page.text()
		array = text.split("|type =")
		first_part = array[0] + "|type = " + Type(c)
		second_part = "\n|series" + array[1].split("|series")[1]
		content = first_part + second_part
		if content != text:
			print(content) if not uploading else EditPage(page, content, 'Modify type to include evil symbols')
			printl("character id: %s" % int(c['id']))

if __name__ == "__main__":
	rewrite_type()