import random, time, requests, asyncio, pyperclip
from packaging.version import InvalidVersion
from googletrans import Translator, LANGUAGES
from tqdm import tqdm

ver = "0.0.3-alpha.5"
exiting = 0
wawa = "wawa" # wawa

#might remove this in the future because file size
#cli = argparse.ArgumentParser(description="BadTranslate CLI")
#cli.add_argument("-s", "--simple", action="store_true", help="Use the simple mode")
#args = cli.parse_args()

def unknownErr():
	print("Error 4: An unknown error ocurred")
def err1(q):
	if q == 0:
		input('Error 1: Unexpected String.')
	elif q == 1:
		input('Error 1: Unexpected String. Press "Enter" to exit.')

try:
	response = requests.get("https://github.com/MrCatOwO/BadTranslate/releases/latest", allow_redirects=False)
	urlHead = response.headers.get("Location")
	if urlHead:
		ghVer = urlHead.rsplit("/", 1)[-1]
		verCompare = ghVer
	else:
		print("Error 2: Could not find version")
except requests.RequestException as e:
	print(f"Error: {e}")
ghVer = ghVer.lstrip("v")
ver = ver.lstrip("v")
try:
	if ghVer > ver:
		verCompare = 1
	elif ghVer < ver:
		verCompare = -1
	elif ghVer := ver:
		verCompare = 2
	else:
		verCompare = 0
except InvalidVersion as e:
	print(f"Error 3: Failed to parse: {e}")
	verCompare = ("")
def checkLangCode(lang):
	return lang in LANGUAGES
	
if verCompare == 1:
	print(f"Outdated version! Please update at github.com/MrCatOwO/BadTranslate/releases/latest ({ver} < {ghVer})")
elif verCompare == -1:
	print(f"You are running a version from the future. You're either a developer, or something messed up big time. ({ver} > {ghVer})")
elif verCompare == 2:
	print(f"You are running the latest version! ({ver})")
elif verCompare == 0:
	print("????? how")
else:
	print("")
def random_language_code():
	languages = list(LANGUAGES.keys())
	return random.choice(languages)

async def translateText(text, iterations, langCode): # do not touch unless you want a really bad time
	translator = Translator()
	translated = text
	for i in tqdm(range(iterations), desc="Translating"):
		try:
			while True:
				randomLang = random_language_code()
				if randomLang != langCode:
					break
			randomTrans = await translator.translate(translated, dest=randomLang)
			resultTrans = await translator.translate(randomTrans.text, dest=langCode)
			translated = resultTrans.text
			tqdm.write(f"Iteration {i + 1}/{iterations}: {translated}")
		except Exception as e:
			tqdm.write(f"Error during translation at iteration {i + 1}: {e}")
			time.sleep(1)
	return translated

def main():
	inputText = input("Enter the text you want to translate: ").strip()
	if not inputText:
		inputText = "null"
	langCode = input("Please select the destination language using short language codes: ").lower().strip()
	if checkLangCode(langCode):
		print(f'Language code "{langCode}" is detected as {LANGUAGES[langCode]}')
	elif langCode == "":
		langCode = "en"
	else:
		print(f'Language code "{langCode}" is not valid.')
		print('Setting language to english.')
		langCode = "en"
	if langCode == "0":
		print("no.")
		langCode = "en"
	iterations = input("Amount of iterations: (Default: 100) ").strip()
	if not iterations:
		iterations = 100
	elif iterations.isdigit():
		iterations = int(iterations)
	else: #                                                                     I don't care that this is technically not an integer;
		print(f'"{iterations}" is not an integer. Setting iterations to 100.')# it's integer enough for me.
		iterations = 100
	if iterations >= 1000:
		print("An extremely high number of iterations has been selected; this might take 30 minutes or more.")
	elif iterations >= 250:
		print("A high number of iterations has been selected; this might take a long time.")
	elif iterations <= 0:
		print("You've selected 0 or fewer iterations; nothing will happen.")
	translated_text = asyncio.run(translateText(inputText, iterations, langCode))
	print("Original text:", inputText)
	print("Translated text:", translated_text)

	pyperclip.copy(translated_text)     
	print("Copied result to clipboard.")

def launcher():
	while True:
		main()
		yn = input('Done. Try another word? (y/n) ').strip().lower()
		if yn == 'y' or yn == 'yes':
			continue
		elif yn == 'n' or yn == 'no':
			print('Exiting now...')
			if verCompare == -1:
				print("Now get back in your DeLorean")
			raise SystemExit
		else:
			err1(1)
launcher()