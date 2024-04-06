from globals import *


def main():
	stories_dict = {}

	for cs in CharacterStory:
		if cs["m_character_id"] in stories_dict:
			stories_dict[cs["m_character_id"]].append({
				"c_id": cs["m_character_id"],
				"id": cs["id"],
				"lv": cs["lv"],
				"title": cs["title"],
				"present_num": cs["present_num"]
				})
		else:
			stories_dict[cs["m_character_id"]] = [{
				"c_id": cs["m_character_id"],
				"id": cs["id"],
				"lv": cs["lv"],
				"title": cs["title"],
				"present_num": cs["present_num"]
			}]

	write_file(stories_dict)
	for key in stories_dict:
		EpisodesRaw(stories_dict[key], key)
		Episode(stories_dict[key])

def write_file(stories_dict):
	count = 0
	string = ""
	for key in stories_dict:
		string += f"|[[File:Chara-ci-{key}.png|90px|link=Template:Character/{key}/Episodes]]\n"
		count += 1
		if count == 6: string += f"|-\n"; count = 0
	with open(PAGES_PATH + "stories.txt", "w") as f:
		f.write(string)

def EpisodesRaw(episodes, key):
	content = f"""<tabber>\n"""
	counter = 0
	for ep in episodes:
		counter += 1
		content += f"""|-| {ep["title"]} = {{{{Character/{key}/Episode/{counter}}}}}\n"""
	content += f"</tabber>"""
	page = wiki.pages[f"Template:Character/{key}/Episodes"]
	print(content) if not uploading else Upload(page, content)

def Episode(array):
	counter = 1
	for ep in array:
		content = Talk(ep)
		page = wiki.pages[f"Template:Character/{ep['c_id']}/Episode/{counter}"]
		print(content) if not uploading else Upload(page, content)
		counter += 1

def Talk(ep):
	return f"""{{|
|-
|Require: Character Lv {ep["lv"]} or Above
|-
|Reward: {ep["present_num"]} Nether Quartz
|-
| <br>
|-
|Dialogue:
{ExtrapolateDialogue(ep)}
|}}
"""

def ExtrapolateDialogue(ep):
	string = f""
	for cst in CharacterStoryTalk:
		if cst["m_character_story_id"] == ep["id"]:
			string += "|-\n|" + cst["talk_text"].replace("\n", "") +"\n|- \n|\n"
	string = string.replace("#NAME#", "Player")
	return string

main()