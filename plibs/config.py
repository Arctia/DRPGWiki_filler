import datetime, json, os

class	Config():
	path = './config.json'

	def __init__(self, path=""):
		self.path = os.path.join(path, self.path)
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

	def add_new_chara(self, c):
		for character in self.js['new_charas']:
			if c['id'] == character['id']:
				return
		chara = {
			'id': c['id'],
			'release_date': c['book'],
		}
		self.js['new_charas'].append(chara)

	def add_mod_chara(self, c):
		for character in self.js['modified_charas']:
			if c['id'] == character['id']: 
				return
		chara = {
			'id': c['id'],
			'modified_date': datetime.datetime.now().strftime("%m-%Y"),
		}
		self.js['modified_charas'].append(chara)

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
