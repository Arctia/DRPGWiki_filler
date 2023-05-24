import datetime, json, os

class	Config():
	path = './config.json'

	def __init__(self, folder=""):
		self.path = os.path.join(folder, self.path)
		self.load_config()

	def __reset__(self):
		self.new_characters()
		self.save_config()

	def	new_characters(self):
		self.js['old_datas']['new_charas'] += self.js['new_charas'].copy()
		self.js['old_datas']['modified_charas'] += self.js['modified_charas'].copy()
		self.js['new_charas'].clear()
		self.js['modified_charas'].clear()

	def remove_duplicates(self):
		pass

	def load_config(self):
		with open(self.path, 'r') as f:
			self.js = json.load(f)

	def save_config(self):
		with open(self.path, 'w') as f:
			json.dump(self.js , f, indent=4)

	def order_by_datetime(self):
		cp = self.js
		cp = sorted(cp['new_charas'], key=lambda x: datetime.strptime(x['release_date'], datetime_f), reverse=True)
		self.js = cp

	def add_new_chara(self, c):
		for character in self.js['new_charas']:
			if c['Character ID'] == character['id']:
				return
		chara = {
			'id': c['Character ID'],
			'release_date': c['book_appear_at'],
		}
		self.js['new_charas'].append(chara)
		self.order_by_datetime()
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

	def get_ids(self):
		data = []
		for chara in self.js['new_charas']:
			data.append(chara['id'])
		return data

	def get_mids(self):
		data = []
		for chara in self.js['modified_charas']:
			data.append(chara['id'])
		return data

	def get_aids(self):
		data = []
		for chara in self.js['new_charas']:
			data.append(chara['id'])
		for chara in self.js['modified_charas']:
			data.append(chara['id'])
		return data
