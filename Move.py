
import time
from globals import *

a_id = [10043, 30001, 30005, 30009, 30013, 30017, 30021, 30025, 30029, 30033, 30037, 
30041, 30045, 30053, 30057, 30061, 30065, 30069, 30073, 30077, 30081, 30085,
30089, 30097, 30105, 30113, 30117, 30125, 30129, 30133, 30049, 30093,
30101, 30109, 30121] 

loop_names = ["A", "B", "C", "D"] 

def main():
	print("starting to move\n")
	reached_id = 30069
	switch = False
	loop_name = False
	loop_n_c = 0
	for c in Charas:
		if c["id"] == reached_id: switch = True
		if not switch: continue

		suf = ""
		if c["id"] in a_id: loop_name = True

		if loop_name:
			suf = "_" + loop_names[loop_n_c]
			loop_n_c += 1
			if loop_n_c == 4: 
				loop_n_c = 0
				loop_name = False

		name = c["name"] + suf

		page = wiki.pages[f'Character/{c["id"]}']
		MovePage(name, page, c["id"])

		print("done moving %s" % c["id"])


def MovePage(name, page, id = 0):
	if page.exists:
		try:
			print(f"""Moving page {id} to {name}""")
			page.move(name, reason="Better Categorization for GL", no_redirect=False)
		except:
			print("moving error, wait 120 Secs to retry")
			time.sleep(120)
			MovePage(name, page, id)

if __name__ == "__main__":
	main()
