from config import Config

print("\nleave empty to skip step\n")
def insert_units(char_type:str = "badass") -> list:	
	clist = []
	while 1:
		inp = input(f"insert new {char_type} id: ")
		if inp == "":
			inp = input(f"new {char_type} chars are {clist}, it's okay? (type y to continue, n to reset the list): ")
			if inp == "y":
				break
			elif inp == "n":
				clist = []
		try:
			clist.append(int(inp))
		except:
			print("invalid input, try again")
	return clist

badasses = insert_units("badass")
print()
gorgeouses = insert_units("gorgeous")
print()

jconf = Config()
jconf.add_badass(clist=badasses)
jconf.add_gorgeous(clist=gorgeouses)
jconf.save_config()