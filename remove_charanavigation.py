# -*- coding: utf-8 -*-
# @Author: arctia
# @Date:   2024-10-24
# @Last Modified by:   arctia
# @Last Modified time: 2024-10-24

from typing import Literal
from mwclient.listing import PageList
from mwclient.page import Page
from globals import *


begin:int = 2
maxin:int = 40000

def update_wiki_character_template(page:Page, id:int = 0) -> bool:
	try:
		content:Literal[''] = page.text()
		if not content:
			print(f"[ERROR ]: character <{id}> page was empty")
			return False

		new_content:Literal[''] = content.replace(
			"{{JP/Characters}}",
			"[[JP/Characters|To Characters List]]",
			)

		page.save(
			new_content,
			summary = "replacing navigation template with a link to it"
			)

		return True
	
	except Exception as e:
		print(f"[ERROR ]: {e}")
	
	return False


for chara in Charas:
	if chara["id"] < begin: continue
	if chara["id"] >= maxin: break

	page:Page = wiki.pages[f'JP/Character/{chara["id"]}']
	status = update_wiki_character_template(page, chara["id"])
	if status:
		print(f"\r[INFO  ]: Updated character <{chara['id']}>", flush=True)
	else:
		print(f"[ERROR ]: Cannot Update character <{chara['id']}>")

	time.sleep(1)