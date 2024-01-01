import time
import mwclient
from globals import wiki, JP, jp_flag, LeaderSkills, translate, Upload, uploading, printl

def main():
	reached_id = 11 # GL 1 #JP 301172
	switch = False

	for l in LeaderSkills:
		if l["id"] == reached_id: switch = True
		if not switch: continue
		
		content = LeaderSkillTemplate(l)

		if not uploading: print(content)
		page = wiki.pages[f'Template:{jp_flag}LeaderSkill/{l["id"]}']
		Upload(page, content)
		print("Evility uploaded: %s" % l["id"])

def create_leader_skill(i, edit=False):
	for l in LeaderSkills:
		if l["id"] == i:
			page = wiki.pages[f'Template:{jp_flag}LeaderSkill/{l["id"]}']
			if not page.exists:
				content = LeaderSkillTemplate(l)
				print(content) if not uploading else Upload(page, content, edit)
				printl("Evility uploaded: %s        " % l["id"])
			if edit:
				content = LeaderSkillTemplate(l)
				if content != page.text():
					print(content) if not uploading else Upload(page, content, edit)
					printl("Evility updated:  %s        " % l["id"])
			break


def LeaderSkillTemplate(l):
	return f"""{{{{LeaderSkillRaw
|id = {l["id"]}
|name = {translate(l["name"])}
|unique_flg = {l["unique_flg"]}
|lv_max = {l["lv_max"]}
|timing_type = {l["timing_type"]}
|trigger_target = {l["trigger_target"]}
|trigger_status = {l["trigger_status"]}
|trigger_param = {l["trigger_param"]}
|target_type = {l["target_type"]}
|effect_type = {l["effect_type"]}
|limit_damage = {l["limit_damage"]}
|effect_correct_type = {l["effect_correct_type"]}
|effect_value_min = {l["effect_value_min"]}
|effect_value_max = {l["effect_value_max"]}
|bad_effect_type = {l["bad_effect_type"]}
|bad_effect_value = {l["bad_effect_value"]}
|description = {Description(l)}
{ArrayList(l["target_params"], "target_params")}
{ArrayList(l["effect_type_params"], "effect_type_params")}
{ArrayList(l["limit_characters"], "limit_characters")}
{ArrayList(l["effect_correct_characters"], "effect_correct_characters")}
{ArrayList(l["effect_turn"], "effect_turn")}
{ArrayList(l["bad_effect_params"], "bad_effect_params")}
}}}}"""

def Description(l):
	if l["id"] in [542, 100262, 100161]:
		val = (l["effect_value_min"]/100)+1
		return translate(l["description"].replace("#PER#", str(val)))
	return translate(l["description"].replace("#PER#", str(l["effect_value_min"])))

def ArrayList(array, text):
	count = 1; string = ""
	for item in array:
		string += f"|{text}_{count} = {str(item)}\n"
		count += 1
	return string

if __name__ == "__main__":
	main()
