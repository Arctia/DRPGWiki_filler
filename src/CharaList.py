
from user_data import *
from globals import *
import mwclient
import time, json, os, sys
from plibs.config import Config
from datetime import datetime

# wiki = mwclient.Site('disgaea-rpg.fandom.com', path='/')
# wiki.login(username=username, password=password)
datetime_f = "%Y-%m-%d %H:%M:%S"
datetime_m = "%Y-%m-%d %H:%M:%S"

def	desktop_view(text:str, id_list:list) -> str:
	for i in id_list:
		if f"{{{{CharacterNavFrameJP|{str(i)}}}}}" in text:
			continue
		text += f"{{{{CharacterNavFrameJP|{str(i)}}}}}"
	text += f"\n</div>"
	return text

def mobile_view(text:str, id_list:list) -> str:
	mobile_last = text.split("|-")[-1]
	counter = mobile_last.count("| ")
	str_to_add = ""
	for i in id_list:
		if f"| {{{{CharacterNavFrameJP|{str(i)}}}}}\n" in text:
			continue 
		if counter == 4:
			str_to_add += "|- \n"
			counter = 0
		str_to_add += f"| {{{{CharacterNavFrameJP|{str(i)}}}}}\n"
		counter += 1

	str_to_add += "|}\n</div>"
	text = text.replace("|}", str_to_add)
	return text

def	uniques_view(id_list:list, new_charas):
	# load wiki page text and divide mobile from desktop
	page = wiki.pages['Template:JP/Characters/Uniques']
	page_uniques = {
		"mobile": mobile_view(page.text().split("</div>")[0], id_list),
		"desktop": desktop_view(page.text().split("</div>")[1].replace("\n", ""), id_list)
	}

	# join mobile and desktop view
	txt = "".join([page_uniques[k] for k in page_uniques])

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

def write_new_section(dates, characters, replace_date=False, previous_date="") -> str:
	ret  = f"|-\n"
	if not replace_date: 
		ret += f"""!style="text-align:left" |Latest Addition {dates}"""
	else:
		ret += previous_date.replace("Latest Addition ", "Latest Addition " + dates + " - ")
	ret += f"\n|-\n"
	ret += f"|{characters}\n"

	return ret

def month_in_page(page, month, year):
	latest_line = page.split("\n")[2]
	return_line = page.split("\n")[4]
	# print(f"[INFO   ]: {latest_line}")
	ld = latest_line.split(" ")[-1]
	if (ld.split("/")[0] == month and ld.split("/")[-1] == year):
		return return_line
	return False

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

	page = wiki.pages['Template:JP/Characters']
	page_text = page.text()

	charas = ""
	dates = ""
	for year in years:

		for month in months:
			dates = ""
			charas = ""
			new_fragment = ""

			for day in days:
				for chara in new_charas:
					if f"{{{{CharacterNavFrameJP|{chara['id']}}}}}" in page_text.split("|}")[0]:
						continue
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
				line_to_replace = month_in_page(page_text, month, year)
				
				if line_to_replace:
					charas += page_text.split("\n")[4].replace("|", "  -  ", 1)
					new_fragment += write_new_section(dates, charas, replace_date=True, previous_date=page_text.split("\n")[2])
					text_to_replace = page_text.split("\n")[1] + "\n" + page_text.split("\n")[2] + "\n" + page_text.split("\n")[3] + "\n" + page_text.split("\n")[4] + "\n"
					page_text = page_text.replace(text_to_replace, new_fragment)
				else:
					dates += f"/{year}"
					new_fragment += write_new_section(dates, charas)
					page_text = "{|\n" + page_text.replace("{|\n", new_fragment, 1)

			# if dates != "": 
			# 	dates += f"/{year}"
			# 	new_fragment += write_new_section(dates, charas)
	
	# page_text = page.text().replace("{|\n", new_fragment, 1)
	Upload(page, page_text)
	path = os.path.join("txt_files", "template.txt")
	with open(path, "w") as f:
		f.write(page_text)
	print("[INFO  ]: Written Main Template Page")

def main():
	jconf = Config("./plibs/")
	jconf.order_by_datetime('new_charas')
	id_list = jconf.get_ids()

	uniques_view(id_list, jconf.js['new_charas'])
	template_view(jconf)

if __name__ == '__main__':
	main()

