import datetime, json, os

datetime_f = "%Y-%m-%d %H:%M:%S"

class	Config():
	path = './config.json'

	def __init__(self, folder=""):
		self.path = os.path.join(folder, self.path)
		self.load_config()

	def __reset__(self):
		self.clear_new()
		# self.clear_modified()
		self.save_config()

	def	clear_modified(self):
		self.js['old_datas']['modified_charas'] += self.js['modified_charas'].copy()
		self.js['modified_charas'].clear()

	def clear_new(self):
		self.js['old_datas']['new_charas'] += self.js['new_charas'].copy()
		self.js['new_charas'].clear()

	def remove_duplicates(self):
		pass

	def load_config(self):
		with open(self.path, 'r') as f:
			self.js = json.load(f)

	def save_config(self):
		with open(self.path, 'w') as f:
			json.dump(self.js , f, indent=4)

	def order_by_datetime(self, key_to_order):
		cp = self.js
		cp = sorted(cp[key_to_order], key=lambda x: datetime.datetime.strptime(x['release_date'], datetime_f), reverse=False)
		self.js[key_to_order] = cp

	def add_new_chara(self, c):
		for character in self.js['new_charas']:
			if c['Character ID'] == character['id']:
				return
		chara = {
			'id': c['Character ID'],
			'release_date': c['book_appear_at'],
		}
		self.js['new_charas'].append(chara)
		self.order_by_datetime('new_charas')
		self.save_config()

	def add_mod_chara(self, c):
		for character in self.js['modified_charas']:
			if c['Character ID'] == character['id']: 
				return
		chara = {
			'id': c['Character ID'],
			'modified_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		}
		self.js['modified_charas'].append(chara)
		self.save_config()

	def get_ids(self) -> list:
		data = []
		print(self.js)
		for chara in self.js['new_charas']:
			data.append(chara['id'])
		return data

	def get_mids(self) -> list:
		data = []
		for chara in self.js['modified_charas']:
			data.append(chara['id'])
		return data

	def get_aids(self) -> list:
		data = []
		for chara in self.js['new_charas']:
			data.append(chara['id'])
		for chara in self.js['modified_charas']:
			data.append(chara['id'])
		return data

	def add_ex_char(self, id:int) -> None:
		if not id in self.js['EX']:
			self.js['EX'].append(id)

	def get_exids(self) -> list:
		return self.js['EX']
