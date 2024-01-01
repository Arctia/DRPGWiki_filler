import time
import mwclient
from globals import *

ids = [3000341, 3000342, 3000343, 3000344]

pp = os.path.join(".", "datas", "GL", "MCommand_1.json")
with open(pp, encoding="utf-8") as f:
	GLCommands = json.load(f)

def main():
	#reached_id =  # JP 
	reached_id = 1 # GL Done
	switch = False
	arr = []

	for s in GLCommands:
		arr.append(s)

	for s in Commands:
		if s["id"] == reached_id: switch = True
		if s["id"] < 200000 or s["id"] > 299999: continue
		if not switch: continue
		#if not s["id"] in ids: continue
		print(s["id"])
		print(s["name"])
		#print(translate(s["name"]))
		for e in arr:
			if e["id"] == s["id"]:
				sp = e

		content = skill_content(s, sp)
		page = wiki.pages[f'Template:JP/Skill/{s["id"]}']

		if page.exists and 1 == 2:
			tt = page.text()
			if tt != content:
				print(content) if not uploading else EditPage(page, content, 'Fix Skill names and xx > xx')
				print("Skill id edit:     %s" % s["id"])
			else:
				print("Skill id passed:   %s" % s["id"])
		else:
			print(content) if not uploading else Upload(page, content)
			print("Skill id uploaded: %s" % s["id"])

def create_skill(i, edit=False, special=False):
	for s in Commands:
		if s["id"] == i:
			page = wiki.pages[f'Template:JP/Skill/{s["id"]}']
			if not page.exists or edit:
				content = skill_content(s, special)
				print(content) if not uploading else Upload(page, content, edit)
				printl("Skill id uploaded: %s        " % s["id"])
			break

def skill_content(s, sp, special=False):
	return SkillTemplateJP(s, sp, special) 

def SkillTemplate(s):
	return f"""{{{{SkillRaw
|id = {s["id"]}
|lv = {{{{{{lv|0}}}}}}
|weapon_mastery_lv = {{{{{{weapon_mastery_lv|0}}}}}}
|name = {s["name"]}
|sp_min = {s["sp_min"]}
|sp_max = {s["sp_max_40"]}
|gain_sp = {s["gain_sp"]}
|attr = {s["attr"]}
|relational_param = {s["relational_param"]}
|description = {translate(s["description"])}
|description_effect = {DescriptionEffect(s)}
{ArrayList(s["effect_values_min"], "effect_values_min")}
{ArrayList(s["effect_values_max_30"], "effect_values_max")}
{ArrayList(s["effect_targets"], "effect_targets")}
{ArrayList(s["command_types"], "command_types")}

{ArrayList(s["effect_values_max_30"], "effect_values_max_30")}
{ArrayList(s["effect_values_max_40"], "effect_values_max_40")}
{ArrayList(s["effect_values_max_50"], "effect_values_max_50")}
{ArrayList(s["variance_rates"], "variance_rates")}
{ArrayList(s["effect_values_sub_min"], "effect_values_sub_min")}
{ArrayList(s["effect_values_sub_max"], "effect_values_sub_max")}

|name_battle = {s["name_battle"]}
|command_category = {s["command_category"]}
|max_lv = {s["max_lv"]}
|circle_flag = {s["circle_flg"]}
|icon_type = {s["icon_type"]}
|resource_id = {s["resource_id"]}
}}}}"""

def SkillTemplateJP(s, sp, special=False):
	return f"""{{{{JP/SkillRaw
|id = {s["id"]}
|lv = {{{{{{lv|0}}}}}}
|weapon_mastery_lv = {{{{{{weapon_mastery_lv|0}}}}}}
|name = {SkillName(sp, special)}
|sp_min = {s["sp_min"]}
|sp_max = {s["sp_max_50"]}
|gain_sp = {s["gain_sp"]}
|attr = {s["attr"]}
|relational_param = {s["relational_param"]}
|description = {sp["description"]}
|description_effect = {DescriptionEffect(sp)}
{ArrayList(s["effect_values_min"], "effect_values_min")}
{ArrayList(s["effect_values_max_50"], "effect_values_max")}
{ArrayList(s["effect_targets"], "effect_targets")}
{ArrayList(s["command_types"], "command_types")}

{ArrayList(s["effect_values_max_30"], "effect_values_max_30")}
{ArrayList(s["effect_values_max_40"], "effect_values_max_40")}
{ArrayList(s["effect_values_max_50"], "effect_values_max_50")}
{ArrayList(s["variance_rates"], "variance_rates")}
{ArrayList(s["effect_values_sub_min"], "effect_values_sub_min")}
{ArrayList(s["effect_values_sub_max"], "effect_values_sub_max")}
{ArrayList(s["trigger_types"], "trigger_types")}
{ArrayList(s["trigger_type_params"], "trigger_type_params")}
{ArrayList(s["trigger_targets"], "trigger_targets")}

|name_battle = {sp["name_battle"]}
|command_category = {s["command_category"]}
|max_lv = {s["max_lv"]}
|circle_flag = {s["circle_flg"]}
|icon_type = {s["icon_type"]}
|resource_id = {s["resource_id"]}
|spell_flag = 1
}}}}"""

def SkillName(s, special=False):
	if not special:
		return s["name"]
	else:
		return f"{{{{Enum/JP/Bios|{s['id']}}}}}"

def DescriptionEffect(s):
	maximum = "effect_values_max_50"
	string = s["description_effect"].replace("#PER1#", f"""{PowerOutput(s['effect_values_min'][0],s[maximum][0])}""")
	if s["effect_values_min"].__len__() > 1:
		count = 0
		for i in s["effect_values_min"]:
			string = string.replace(f"#PER{count+1}#", f""" {PowerOutput(s['effect_values_min'][count],s[maximum][count])}""")
			count +=1
	return string

def PowerOutput(v1, v2):
	result = v1 if v1 == v2 else f"{v1}>{v2}"
	if result != None:
		return result
	else:
		return f""

def ArrayList(array, text):
	count = 1; string = ""
	for item in array:
		string += f"|{text}_{count} = {str(item)}\n"
		count += 1
	return string

if __name__ == "__main__":
	main()
