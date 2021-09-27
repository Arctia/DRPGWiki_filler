from globals import *

dates = {}

for c in Charas:
	if c["m_leader_skill_id"] != 0 and c["id"] < 40000:
		date = c["book_appear_at"].split(" ")[0]
		if date == "2019-08-20": date = "2020-08-20"
		if not date in dates: dates[date] = []
		dates[date].append(c)

#print(dates)

def ordering(_dict_):
	_my_dates = []
	while 1:
		ly, lm, ld = 0, 0, 0
		for key in _dict_:
			year, month, day = key.split("-")
			year = int(year); month = int(month); day = int(day)
			if key in _my_dates: continue
			if year == 2119: continue
			if year > ly: 
				ly = year; lm = month; ld = day
			elif year == ly:
				if month > lm:
					lm = month; ld = day
				elif month == lm:
					if day > ld:
						ld = day
		if ly != 0:
			_my_dates.append("%s-%s-%s" % (ly, lm if lm > 9 else "0"+str(lm), ld if ld > 9 else "0"+str(ld)))
		else:
			break

	return _my_dates

def WriteDay(key):
	year, month, day = key.split("-")
	return f"{month}/{day}/{year}"

def GetCharas(day):
	s = ""
	for cid in dates[day]:
		#s += f"{{{{CharacterNavBoxJP|{c["id"]}}}}}"
		s += f"""{{{{CharacterNavBoxFrame|{cid["id"]}|Weapon={cid["best_weapon_type"]}|kind={"human" if cid['character_type'] == 1 else 'monster'}|JP=true|rarity=4|type={EnumEvilSymbol[cid["m_potential_class_id"]]}}}}}"""
	return s

ordered_dates = ordering(dates)

string = f"""{{| class="wikitable"\n"""

for d in ordered_dates:
	string += f"""|-\n!style="text-align:left" |{WriteDay(d)}\n|-\n|{GetCharas(d)}\n"""

string += f"|}}"

with open("./txt_files/CharaRelease.txt", "w", encoding="utf-8") as file: 
	file.write(string)

page = wiki.pages["Japan_Characters_Release_Date"]
content = string
Upload(page, content, True)