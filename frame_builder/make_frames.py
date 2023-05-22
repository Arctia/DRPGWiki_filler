
import sys
import json, os
from PIL import Image
from PIL import ImageOps
sys.path.insert(1, os.path.join(".."))

from plibs.config import Config

fd_plibs = os.path.join("..", "plibs")

io = Image.open
jconf = Config(folder = fd_plibs)

BADASS = jconf.js["base_type"]["BADASS"]
GORGEOUS = jconf.js["base_type"]["GORGEOUS"]
ids = jconf.get_ids()

with open(os.path.join("..", "datas", "JP", "character.json"), encoding="utf-8") as file:
	Characters = json.load(file)["DataList"]

class Pos(object):
	"""docstring for Pos"""
	def __init__(self, arg, arg2):
		super(Pos, self).__init__()
		self.x = arg
		self.y = arg2
		
class Chara(object):
	id = 1
	fr = 6
	wp = 1
	tp = 1
	ev = 2
	
	def __init__(self, c):
		super(Chara, self).__init__()
		self.id = c["id"]
		self.fr = c["base_rare"]
		self.wp = c["best_weapon_type"]
		self.ev = c["m_potential_class_id"]
		self.tp = c["character_type"]
		self.check_badass()

	def check_badass(self):
		if c["id"] in BADASS:
			self.fr = 5
		elif c["id"] in GORGEOUS:
			self.fr = 6

of 			= Pos(16 ,	27)
cut_face 	= Pos(178,	200)
icon_size 	= (36 ,	36)

_void 		= "./void.png"
_bg			= "./bg.png"

_p_faces	= os.path.join(fd_plibs, "assets", "assetbundles",
	"images", "chara", "face")


_p_frames 	= "./frame/"
_p_weap 	= "./weapon/"
_p_evil 	= "./evil_symbol/"
_p_kind		= "./kind/"

frame_path	= os.path.join(fd_plibs, "assets", "assetbundles",
	"images", "chara", "frames")

def crop_face(img):
	w = img.width
	crop_size = (w - 175) if w > 175 else 0
	border = (4, 0, crop_size, 0)
	return ImageOps.crop(img, border)

def create_image(chara):
	void = io(_void)
	bg 	 = io(_bg)

	face = io(_p_faces + f"{chara.id}.png")
	face = crop_face(face)

	frame = io(_p_frames + f"{chara.fr}.png")
	frame = frame.resize((210,242), Image.ANTIALIAS)

	weapon = io(_p_weap + f"{chara.wp}.png")
	weapon = weapon.resize(icon_size, Image.ANTIALIAS)

	evil = io(_p_evil + f"{chara.ev}.png")
	evil = evil.resize(icon_size, Image.ANTIALIAS)

	kind = io(_p_kind + f"{chara.tp}.png")
	kind = kind.resize((32,32), Image.ANTIALIAS)

	void.paste(bg, (0,0), bg)
	void.paste(face, (of.x, of.y), face)
	void.paste(frame, (0,0), frame)
	void.paste(weapon, (7,45), weapon)
	void.paste(evil, (7, 93), evil)
	void.paste(kind, (5, 5), kind)

	os.makedirs(frame_path, exist_ok = True)
	void.save(f"{frame_path}/{chara.id}.png")
	#void.show()

for c in Characters:
	if not c["id"] in ids: continue
	if c["id"] >= 40000: continue
	if c["m_potential_class_id"] == 0: continue
	chara = Chara(c)
	create_image(chara)


