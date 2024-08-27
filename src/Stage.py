
from globals import *
import StageEnemy

stage_number = 2
Stages = []

for x in range(stage_number):
	with open("./datas/GL/MStage_" + str(x+1) + ".json", encoding="utf-8") as file:
		Stages += json.load(file)

stage_mission_number = 3
StageMissions = []

for x in range(stage_mission_number):
	with open("./datas/GL/MStageMission_" + str(x+1) + ".json", encoding="utf-8") as file:
		StageMissions += json.load(file)

episodes_list = {}

def main():
	switch = False; reached_id = 308407
	for s in Stages:
		if s["id"] == reached_id: switch = True
		if not switch: continue
		if not str(s["id"]).__len__() == 6: continue 
		if s["m_story_id"] != 0: continue
		
		Create_Info(s["id"])
		Create_Waves(s)
		Create_Stage(s)

		#if str(s["id"]).__len__() == 6:
		#	SubEpisode(s)
		printl("Stage id:   %s                    " % s["id"])
	
	CreateEpisodesPages()

"""###########################################################################
############### ° Episodes
###########################################################################"""

def SubEpisode(s):
	story = int(str(s["id"])[0]) # 1 easy 2 normal 3 hard
	episode = int(str(s["id"])[1] + str(s["id"])[2])
	sub_episode = int(str(s["id"])[3])
	stage = int(str(s["id"])[4] + str(s["id"])[5])

	check_presence(story, episode, sub_episode, stage)

def check_presence(st, ep, sep, stage):
	if not st in episodes_list:
		episodes_list[st] = {}
	if not ep in episodes_list[st]:
		episodes_list[st][ep] = {}
	if not sep in episodes_list[st][ep]:
		episodes_list[st][ep][sep] = []

	episodes_list[st][ep][sep].append(stage)

def CreateEpisodesPages():
	l = episodes_list
	for mode in l:
		if mode == 1: smode = "Easy"
		if mode == 2: smode = "Normal"
		if mode == 3: smode = "Hard"
		ModePage(l[mode], mode, smode)
		for ep in l[mode]:
			EpisodePage(l[mode][ep], ep,smode)
			for sep in l[mode][ep]:
				SubEpisodePage(l[mode][ep][sep], mode, ep, sep, smode)

def ModePage(l, mode, smode):
	content = f"<tabber>\n"
	for i in l:
		content += f"|-|Episode {i}= {{{{MainStory/{smode}/Episode/{i}}}}}\n"
	content += f"</tabber>"
	page = wiki.pages[f"Template:MainStory/{smode}"]
	upload(page, content)
	printl("Mode id:   %s                    " % smode)

def EpisodePage(l, ep, smode):
	content = f"<tabber>\n"
	for i in l:
		content += f"|-|Sub Episode {i}= {{{{MainStory/{smode}/Episode/{ep}/SubEpisode/{i}}}}}\n"
	content += f"</tabber>"
	page = wiki.pages[f"Template:MainStory/{smode}/Episode/{ep}"]
	upload(page, content)
	printl("Epis id:   %s                    " % ep)

def SubEpisodePage(l, mode, ep, sep, smode):
	content = f"<tabber>\n"; c = 1
	if ep < 10: eps = "0" + str(ep)
	else: eps = str(ep)
	for i in l:
		if i < 10: i = "0" + str(i)
		content += f"|-|Stage {c}= {{{{Stage/{mode}{eps}{sep}{i}}}}}\n"
		c += 1
	content += f"</tabber>"
	page = wiki.pages[f"Template:MainStory/{smode}/Episode/{ep}/SubEpisode/{sep}"]
	upload(page, content)

"""###########################################################################
############### ° Stage
###########################################################################"""

def Create_Stage(s):
	content = Stage(s)
	page = wiki.pages[f"Template:Stage/{s['id']}"]
	upload(page, content, True)

def Stage(s):
	return f"""{{{{StageRaw
| id = {s["id"]}
| m_area_id = {s["m_area_id"]}
| m_story_id = {s["m_story_id"]}
| rank = {s["rank"]}
| proper_level = {s["proper_level"]}
| appear_m_stage_id = {s["appear_m_stage_id"]}
| name = {s["name"]}
| bgm = {s["bgm"]}
| boss_bgm = {s["boss_bgm"]}
| bg_id = {s["bg_id"]}
| no = {s["no"]}
| act = {s["act"]}
| exp = {s["exp"]}
| lose_m_story_id = {s["lose_m_story_id"]}
| present_types = {s["present_types"]}
| present_ids = {s["present_ids"]}
| present_rarities = {s["present_rarities"]}
| present_nums = {s["present_nums"]}
| sort = {s["sort"]}
| description = {s["description"]}
| display_info_flg = {s["display_info_flg"]}
}}}}
"""

"""###########################################################################
############### ° Stage Waves
###########################################################################"""

def Create_Waves(s):
	# write mobs in that stage, looking for the last to check the wave
	elist = StageEnemy.WriteEnemies(s["id"])
	WaveIds(s["id"], elist)
	WavePage(s, elist)

def WavePage(s, elist):
	waves_number = int(str(elist[-1])[-3])
	content = f"""<tabber>\n"""
	for w in range(waves_number):
		content += f"""|-|Wave {w+1}= {{{{Stage/{s["id"]}/Wave/{w+1}}}}}\n"""
	content += f"</tabber>"
	page = wiki.pages[f'Template:Stage/{s["id"]}/Waves']
	upload(page, content, True)

def WaveIds(sid ,enemies):
	waves = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
	for e in enemies:
		wave_id = int(str(e)[-3])
		waves[wave_id].append(e)

	for key in waves:
		if waves[key].__len__()>0:
			Wave(sid, waves[key], key)

def Wave(sid, enemies, wave):
	page = wiki.pages[f"Template:Stage/{sid}/Wave/{wave}"]
	content = f"""{{| class ="wikitable" style="width:100%; text-align:center;"\n"""
	for e in enemies:
		content += f"""| style="width:20%" | {{{{Stage/Enemy/{e}}}}}\n"""
	content += f"|}}"
	upload(page, content, True)

"""###########################################################################
############### ° Stage Missions
###########################################################################"""

def Create_Info(id, mn = 1):
	content = f"""{{{{Stage/InfoRaw\n"""
	for sm in StageMissions:
		if id != sm["m_stage_id"]: continue
		content += StageInfo(sm, mn)
		if mn == 3: break
		mn += 1
	content += f"}}}}"
	page = wiki.pages[f'Template:Stage/{id}/Info']
	upload(page, content, True)

def StageInfo(s, n):
	return f"""
| title_{n} = {s["title"]}
| present_id_{n} = {s["present_id"]}
| present_num_{n} = {s["present_num"]}
| id_{n} = {s["id"]}
| m_stage_id_{n} = {s["m_stage_id"]}
| condition_type_{n} = {s["condition_type"]}
| condition_num_{n} = {s["condition_num"]}
| present_rarity_{n} = {s["present_rarity"]}
| sort_{n} = {s["sort"]}
"""

def upload(page, content, edit=False):
	print(content) if not uploading else Upload(page, content, edit)

if __name__ == "__main__":
	main()