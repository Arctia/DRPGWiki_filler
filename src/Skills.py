
from globals import *

ids = [3000341, 3000342, 3000343, 3000344]

def main():
	#reached_id =  # JP 
	reached_id = 1 # GL Done
	switch = False

	for s in Commands:
		if s["id"] == reached_id: switch = True
		if not switch: continue
		if not s["id"] in ids: continue 
		
		content = skill_content(s)
		page = wiki.pages[f'Template:{jp_flag}Skill/{s["id"]}']

		if page.exists:
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
			page = wiki.pages[f'Template:{jp_flag}Skill/{s["id"]}']
			if not page.exists or edit:
				content = skill_content(s, special)
				print(content) if not uploading else Upload(page, content, edit)
				printl("Skill id uploaded: %s        " % s["id"])
			break

def skill_content(s, special=False):
	if JP: return SkillTemplateJP(s, special)
	else: return SkillTemplate(s) 

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

def SkillTemplateJP(s, special=False):
	return f"""{{{{JP/SkillRaw
|id = {s["id"]}
|lv = {{{{{{lv|0}}}}}}
|weapon_mastery_lv = {{{{{{weapon_mastery_lv|0}}}}}}
|name = {SkillName(s, special)}
|sp_min = {s["sp_min"]}
|sp_max = {s["sp_max_50"]}
|gain_sp = {s["gain_sp"]}
|attr = {s["attr"]}
|relational_param = {s["relational_param"]}
|description = 
|description_effect = {DescriptionEffect(s)}
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

|name_battle = 
|command_category = {s["command_category"]}
|max_lv = {s["max_lv"]}
|circle_flag = {s["circle_flg"]}
|icon_type = {s["icon_type"]}
|resource_id = {s["resource_id"]}
}}}}"""

def SkillName(s, special=False):
	if not special:
		return translate(s["name"])
	else:
		return f"{{{{Enum/JP/Bios|{s['id']}}}}}"

def DescriptionEffect(s):
	maximum = "effect_values_max_50" if JP else "effect_values_max_40"
	string = s["description_effect"].replace("#PER1#", f"""{PowerOutput(s['effect_values_min'][0],s[maximum][0])}""")
	if s["effect_values_min"].__len__() > 1:
		count = 0
		for i in s["effect_values_min"]:
			string = string.replace(f"#PER{count+1}#", f""" {PowerOutput(s['effect_values_min'][count],s[maximum][count])}""")
			count +=1
	return translate(string)

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
