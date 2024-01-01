
from globals import *
import StageEnemy


bpath = "./datas/JP/"

with open(bpath + "stage.json", encoding="utf-8") as file:
	Stages = json.load(file)["DataList"]

with open(bpath + "stagemission.json", encoding="utf-8") as file:
	StageMissions = json.load(file)["DataList"]

with open(bpath + "eventmission.json", encoding="utf-8") as file:
	MEventMissions = json.load(file)["DataList"]

with open(bpath + "eventboostcharacter.json", encoding="utf-8") as file:
	EventBoostCharas = json.load(file)["DataList"]

with open(bpath + "eventmissiondaily.json", encoding="utf-8") as file:
	MEventDailyMissions = json.load(file)["DataList"]

with open(bpath + "product.json", encoding="utf-8") as file:
	MEventShops = json.load(file)["DataList"]

with open(bpath + "area.json", encoding="utf-8") as file:
	MStory = json.load(file)["DataList"]

EV_ID = int(input("Insert the event id: "))
STAGE_PER_SECTION = int(input("Insert stages per section: "))
#Event_Stage_Pic = input("Insert the name of the stage pic on Fandom: ").replace(".png", "")
Event_Stage_Pic = f"Event_{EV_ID}_map_icon"

EV_SHOP_ID 			= 100 + EV_ID
event_start_at 		= 1000101101 + (EV_ID*1000000)
event_hard_at 		= 1000201101 + (EV_ID*1000000)
event_rec 			= 10001 + (EV_ID*10); 			event_rec2 	= 10002 + (EV_ID*10)
event_chapter_name 	= 100010 + (EV_ID*100)

#Event_Stage_Pic = "NBP_Map_icon"

def main():
	easy_stages 	= []; easy_missions 	= []
	normal_stages 	= []; normal_missions 	= []
	hard_stages 	= []; hard_missions 	= []
	shard_stages 	= []; shard_missions 	= []

	switch = False; reached_id = event_start_at
	for s in Stages:
		if s["id"] == reached_id: switch = True
		if not switch: continue
		if not str(event_rec) in str(s["id"]) and not str(event_rec2) in str(s["id"]): break
		if s["m_story_id"] != 0: continue

		if int(str(s["id"])[-6]) == 2:
			shard_stages.append(s)
			shard_missions.append(GetMissions(s))
		elif int(str(s["id"])[-3]) == 1: 
			easy_stages.append(s)
			easy_missions.append(GetMissions(s))
		elif int(str(s["id"])[-3]) == 2: 
			normal_stages.append(s)
			normal_missions.append(GetMissions(s))
		elif int(str(s["id"])[-3]) == 3: 
			hard_stages.append(s)
			hard_missions.append(GetMissions(s))

	print("[INFO	] Writing Stages...")
	content = f"<tabber>\n"
	content += Table(easy_stages, easy_missions, "Easy")
	content += Table(normal_stages, normal_missions, "Normal")
	content += Table(hard_stages, hard_missions, "Hard")
	content += Table(shard_stages, shard_missions, "Super Hard Mode")
	content += f"</tabber>"

	content += f"""\n<tabber>\n"""

	print("[INFO	] Writing Characters Boost...")
	content += CharacterBoost()
	print("[INFO	] Writing Dailies...")
	content += DailyMissions()
	print("[INFO	] Writing Event Missions...")
	content += EventMissions()
	print("[INFO	] Writing Event Shop...")
	content += EventShop()

	content += f"""</tabber>"""

	#print(content)
	print("[INFO	] Printing result to ./txt_files/event.txt ...")
	with open("./txt_files/event.txt", "w", encoding="utf-8") as f:
		f.write(content)

def EventShop():
	return f"""|-| Event Shop = {{| {TableClass()}
|-
|+
!Item
!Name
!Points
!Limit
{ShopItem()}|}}\n
"""

def ShopItem(string = f""):
	for i in MEventShops:
		if not i["m_item_shop_id"] == EV_SHOP_ID: continue
		string += f"""|- \n| [[File:Item icon-normal-{i["icon_no"]}.png|80px]]\n"""
		string += f"""| {translate(i["name"])}\n"""
		string += f"""| {i["price"]}\n"""
		string += f"""| {i["limit_num"]}\n"""
	return string

def DailyMissions():
	return f"""|-| Daily Missions= {{| {TableClass()}
! Mission
! Reward
{Dailies()}|}}\n
"""

def Dailies():
	ids = {2003: "Event Points", 201: "Nether Quartz", 301: "AP Potion", 108: "BG ???", 4914: "Tickets"}
	for j in range(2008, 2100): ids[j] = "Event Points"
	string = f""
	for dm in MEventDailyMissions:
		if dm["m_event_id"] == EV_ID:
			string += f"""|- \n| {dm["title"]}\n"""
			sss = ids[dm["present_id"]] if dm["present_id"] in ids else "???"
			string += f"""| {sss} x{dm["present_num"]}\n"""
	return string

def EventMissions():
	return f"""|-| Total Missions= {{| {TableClass()}
! Mission
! Reward
{Missions()}|}}\n"""

def Missions():
	ids = {2003: "Event Points", 201: "Nether Quartz", 301: "AP Potion", 108: "Music", 1602: "???"}
	for j in range(2008, 2100): ids[j] = "Event Points"
	string = f""
	for evm in MEventMissions:
		if evm["m_event_id"] == EV_ID:
			string += f"""|- \n| {evm["title"]}\n"""
			sss = ids[evm["present_id"]] if evm["present_id"] in ids else "???"
			string += f"""| {ids[evm["present_id"]]} x{evm["present_num"]}\n"""
	return string

def CharacterBoost():
	return f"""|-|Info = {{| {TableClass()}
|-
! style="background:#dfdbdb" |Special Characters
|-
|
* The following characters reward +XX% Bonus Event Points in the Event.

{Characters()}

* There's a chance a Wave of pink Prinnies will appear, rewarding extra Event Points than usual.

* Depending on the difficulty of the challenges, there'll be one stage increasing the bonus of higher PT everyday.
|}}\n"""

def Characters():
	string = f"{{|\n"; imgsize = 80
	for cb in EventBoostCharas:
		if cb["m_event_id"] == EV_ID:
			string += f"""|{{{{CharacterBonusPt| cid={cb["m_character_id"]}| percentage={cb["effect_value"]}}}}}\n""" #NavBox|{cb["m_character_id"]}|imgsize={imgsize}px}}}} + {cb["effect_value"]}%\n"""
	string += f"|}}"
	return string

def GetMissions(s):
	lista = []; c = 1
	for sm in StageMissions:
		if sm["m_stage_id"] == s["id"]:
			lista.append(sm["title"])
			c += 1
		if c == 4: break
	return lista

def TableClass():
	return f"""style="padding: 1px;background: #F7F7F7;border: 2px solid #414141;border-radius: 7px;-moz-border-radius: 7px;-webkit-border-radius: 7px; box-shadow:0 0 4px #414141;" border="2" width="100%" align="center" """

def StartTable(epname="Title"):
	return f"""{{{{{{!}}}} {TableClass()}
{{{{!}}}}- style="background:#dfdbdb"
{{{{!}}}}+[[File:{Event_Stage_Pic}.png{{{{!}}}}42x42px]] '''{epname}''' [[File:{Event_Stage_Pic}.png{{{{!}}}}42x42px]]
{{{{!}}}}Stage Name
{{{{!}}}}Enemy Lv.
{{{{!}}}}AP
{{{{!}}}}EXP
{{{{!}}}}Ev. Points
{{{{!}}}}Missions\n"""


def Table(stages, missions, mode="Easy"):
	#print(missions)
	titles = []
	for i in range(1,6):
		for st in MStory:
			if st["id"] == (event_chapter_name*10+i):
				titles.append(st["name"])
	content = f"|-|{mode} = {{{{#tag:tabber|"
	for ep in range(5):
		content += f"""{{{{!}}}}-{{{{!}}}}{titles[ep]} = """
		content += StartTable(titles[ep])
		wide = STAGE_PER_SECTION if not ep == 4 else STAGE_PER_SECTION + 3
		if mode == "Super Hard Mode": wide = 3
		for c in range(wide):
			content += FillStage(stages[c+(ep*STAGE_PER_SECTION)], missions[c+(ep*STAGE_PER_SECTION)])
		content += f"""{{{{!}}}}-
{{{{!}}}} colspan="6" <div style="text-align: center;"> {{{{!}}}}Area Clear Reward: [[File:Nether Quartz L.png|50px]] Nether Quartz 50x </div>
"""
		if mode == "Super Hard Mode": break
	content += "}}"
	return content

def FillStage(stage, missions):
	return f"""{{{{!}}}}-
{{{{!}}}} {stage["name"]}
{{{{!}}}} {stage["proper_level"].replace('"', '')}
{{{{!}}}} {stage["act"]}
{{{{!}}}} {stage["exp"]}
{{{{!}}}} ToDo
{{{{!}}}}
* {MissionTranslate(missions[0])} (Nether Quartz x10)
* {MissionTranslate(missions[1])} (Nether Quartz x10)
* {MissionTranslate(missions[2])} (Nether Quartz x10)\n"""

def MissionTranslate(mission):
	if mission == "戦闘不能2人以下で勝利":
		return "Less than 2 members defeated"
	elif mission == "戦闘不能1人以下で勝利":
		return "1 or less member defeated"
	elif mission == "1人も戦闘不能にならずに勝利":
		return "All members surviving"

if __name__ == "__main__":
	main()
