
from globals import *

with open("./datas/JP/event.json", encoding="utf-8") as file:
	EV = json.load(file)["DataList"]

def UploadImage(file, EV_ID):
	name = f"Event_{EV_ID}_map_icon"
	try:
		page = wiki.pages[f"File:{name}.png"]
		if page.exists == False:
			ff = file
			print(ff)
			wiki.upload(file=ff, filename=name, ignore=True)
	except requests.exceptions.ReadTimeout:
		UploadImage(file)
	except mwclient.errors.APIError:
		print("Failed to upload wait 120 secs to retry")
		time.sleep(120)
		UploadImage(file)

def main():
	for e in EV:
		if not e["event_type"] == 1: continue
		path = "./res/story_event/" + e["resource_name"] + "/"
		file = path + "map_icon.png"
		UploadImage(file, e["id"])

main()