
import os, dotenv, requests
from user_data import excell_url

def download_excell() -> bool:
	print("[INFO  ]: Trying to download latest translation")
	try:
		response = requests.get(excell_url)
	except Exception as e:
		print(f"[ERROR ]: error while downloading the excell file -> {e}")
		return False

	try:
		with open(os.path.join("translation_sheet", "Disgaea RPG Translations of Characters.xlsx"), "wb") as f:
			f.write(response.content)
	except Exception as e:
		print(f"[ERROR ]: error while saving the file -> {e}")
		return False

	print("[INFO  ]: Downloaded latest xlsx file")
	return True

if __name__ == "__main__":
	dotenv.load_dotenv()
	download_excell()
