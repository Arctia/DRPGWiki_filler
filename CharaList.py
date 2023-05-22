
from user_data import *
from globals import *
import mwclient
import time, json, os, sys
from plibs.config import Config
from datetime import datetime

# wiki = mwclient.Site('disgaea-rpg.fandom.com', path='/')
# wiki.login(username=username, password=password)
datetime_f = "%Y-%m-%d %H:%M:%S"
datetime_m = "%m-%Y"

def	desktop_view(text:str, id_list:list) -> str:
	for i in id_list:
		text += f"{{{{CharacterNavFrameJP|{str(i)}}}}}"
	text += f"\n</div>"
	return text

def mobile_view(text:str, id_list:list) -> str:
	mobile_last = text.split("|-")[-1]
	counter = mobile_last.count("| ")
	str_to_add = ""
	for i in id_list:
		if counter == 4:
			str_to_add += "|- \n"
			counter = 0
		str_to_add += f"| {{{{CharacterNavFrameJP|{str(i)}}}}}\n"
		counter += 1

	str_to_add += "|}\n</div>"
	text = text.replace("|}", str_to_add)
	return text

def	uniques_view(id_list:list):
	# load wiki page text and divide mobile from desktop
	page = wiki.pages['Template:JP/Characters/Uniques']
	page_uniques = {
		"mobile": mobile_view(page.text().split("</div>")[0], id_list),
		"desktop": desktop_view(page.text().split("</div>")[1].replace("\n", ""), id_list)
	}

	# join mobile and desktop view
	txt = "".join([page_uniques[k] for k in page_uniques])
	# print(txt)

	# upload new text
	Upload(page, txt)
	print("[INFO  ]: Written Uniques Page")

def check_date(date, tp="month", value="00") -> bool:
	if tp == "month": tp = "%m"
	if tp == "year": tp = "%Y"
	if tp == "day": tp = "%d"

	if datetime.strptime(date, datetime_f).strftime(tp) == value:
		return True

	return False

def write_new_section(dates, characters) -> str:
	return f"""|-
!style="text-align:left" |Latest Addition {dates}
|-
|{characters}\n"""

def template_view(jconf:object):
	js = jconf.js

	new_charas = sorted(js['new_charas'], key=lambda x: datetime.strptime(x['release_date'], datetime_f), reverse=False)
	mod_charas = sorted(js['modified_charas'], key=lambda x: datetime.strptime(x['modified_date'], datetime_m), reverse=True)

	years = set(datetime.strptime(d['release_date'], datetime_f).strftime('%Y') for d in js['new_charas'])
	months = set(datetime.strptime(d['release_date'], datetime_f).strftime('%m') for d in js['new_charas'])
	days = set(datetime.strptime(d['release_date'], datetime_f).strftime('%d') for d in js['new_charas'])

	years = sorted(years, key=lambda x: int(x), reverse = True)
	months = sorted(months, key=lambda x: int(x), reverse = True)
	days = sorted(days, key=lambda x: int(x), reverse = True)

	new_fragment = "{|\n"

	charas = ""
	dates = ""
	for year in years:

		for month in months:
			dates = ""
			charas = ""
			for day in days:
				for chara in new_charas:
					if (check_date(chara['release_date'], "day", day) and 
						check_date(chara['release_date'], "month", month) and
						check_date(chara['release_date'], "year", year)):
						tmp = f"{month}/{day}"
						if not tmp in dates:
							if dates != "": 
								dates += " - "
								charas += "  -  "
							dates += f"{tmp}"
						charas += f"{{{{CharacterNavFrameJP|{chara['id']}}}}}"

			if dates != "": 
				dates += f"/{year}"
				new_fragment += write_new_section(dates, charas)

	page = wiki.pages['Template:JP/Characters']
	page_text = page.text().replace("{|\n", new_fragment, 1)
	Upload(page, page_text)
	print("[INFO  ]: Written Main Template Page")


def main():
	jconf = Config("./plibs/")
	id_list = jconf.get_ids()

	uniques_view(id_list)
	template_view(jconf)

if __name__ == '__main__':
	main()

