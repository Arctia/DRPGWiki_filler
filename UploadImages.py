
import os
import mwclient
import requests
from globals import wiki

res_path = "./res/"

folders = ["ci", "illust", "command", "face"]
ico_folder = "icons"

img_replace = False

def main():
	for folder in folders:
		for file in os.listdir(res_path+folder+"/"):
			if file[-4:] != ".png": continue
			UploadImage(file, folder)

def UploadImage(file, folder=""):
	name = change_name(file)
	name = f"Chara-{folder}-{name}"
	try:
		page = wiki.pages[f"File:{name}"]
		if page.exists == False or img_replace == True:
			ff = res_path+folder+"/"+file
			print(ff)
			wiki.upload(file=ff, filename=name, ignore=True)
	except requests.exceptions.ReadTimeout:
		UploadImage(file)
	except mwclient.errors.APIError:
		print("Failed to upload wait 120 secs to retry")
		time.sleep(120)
		UploadImage(file)

def change_name(path):
	if " #" in path:
		s = path.split(" #")
		s = s[0]+ ".png"
		return s
	else:
		return path

def Upload_Icon(file, folder=""):
	name = f"Item_icon-normal-{file}"
	try:
		page = wiki.pages[f"File:{name}"]
		if page.exists == False:
			ff = res_path+folder+"/"+file
			print(ff)
			wiki.upload(file=ff, filename=name, ignore=True)
	except requests.exceptions.ReadTimeout:
		UploadImage(file)
	except mwclient.errors.APIError:
		print("Failed to upload wait 120 secs to retry")
		time.sleep(120)
		UploadImage(file)


def upload_icons():
	for file in os.listdir(res_path+ico_folder+"/"):
		if file[-4:] != ".png": continue
		Upload_Icon(file, ico_folder)


inp = input("c for Characters, i for icons: ")
if inp == "c":
	main()
elif inp == "i":
	upload_icons()
