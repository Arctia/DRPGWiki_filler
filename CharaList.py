
from user_data import *
# from globals import *
import mwclient
import time, json, os, sys
from plibs.config import Config

wiki = mwclient.Site('disgaea-rpg.fandom.com', path='/')
#wiki.login(username=username, password=password)

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
	print(txt)

	# upload new text
	# Upload('Template:JP/Characters/Uniques', txt)

def main():
	id_list = Config("./plibs/").get_ids()

	uniques_view(id_list)





if __name__ == '__main__':
	main()
