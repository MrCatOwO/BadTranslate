import random, time, requests, asyncio, pyperclip, platform
from googletrans import Translator, LANGUAGES
from tqdm import tqdm

ver = "0.0.3-alpha.5"
exiting = 0

try:
	response = requests.get("https://github.com/MrCatXj/BadTranslate/releases/latest", allow_redirects=False)
	urlHead = response.headers.get("Location")
	ghVer = urlHead.rsplit("/", 1)[-1].lstrip("v")
except requests.RequestException as e:
	print(f"Could not fetch latest GitHub release: {e}")
ver1 = ver.lstrip("v")
	
try:
	if ghVer > ver1:
		print(f"Outdated version! Please update at https://github.com/MrCatXj/BadTranslate/releases/latest ({ver} < {ghVer})")
	elif ghVer < ver1:
		print(f"You are running a version from the future. You're either a developer, or something messed up big time. ({ver} > {ghVer})")
	elif ghVer == ver1:
		print(f"You are running the latest version! ({ver})")
	else:
		print("????? how")
except NameError as e:
	print(f"Could not compare versions: {e}")


# no touchy zone begins here

async def translateText(text, iterations, langCode):
	translator = Translator()
	resultTrans = text
	for i in tqdm(range(iterations), desc="Translating" , bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt} | {elapsed} elapsed | ETA: {remaining}"):
		try:
			while True:
				randomLang = random.choice(list(LANGUAGES))
				if randomLang != langCode:
					break
			randomTrans = await translator.translate(resultTrans, dest=randomLang)
			resultTrans = await translator.translate(randomTrans.text, dest=langCode)
			resultTrans = resultTrans.text
			tqdm.write(f"Iteration {i + 1}/{iterations} ({LANGUAGES[randomLang]} to {LANGUAGES[langCode]}): {resultTrans}")
		except Exception as e:
			tqdm.write(f"Error during translation at iteration {i + 1}: {e}")
			time.sleep(1)
	return resultTrans

#hours_wasted_here = 9
# no touchy zone ends here

def main():
	inputText = input("Enter the text you want to translate: ").strip()
	if not inputText:
		inputText = "null"
	langCode = input("Please select the destination language (ISO 639-1 code): ").lower().strip()
	if langCode in LANGUAGES:
		print(f'Language code "{langCode}" is detected as {LANGUAGES[langCode]}')
	elif langCode == "":
		langCode = asyncio.run(langDetect(inputText))
	else:
		print(f'Language code "{langCode}" is not valid.')
		print('Setting language to english.')
		langCode = "en"
	iterations = input("Amount of iterations: (Default: 100) ").strip()
	if not iterations:
		iterations = 100
	elif iterations.isdigit():
		iterations = int(iterations)
	else: #                                                                      I don't care that this is technically not an integer;
		print(f'"{iterations}" is not an integer. Setting iterations to 100.') # it's integer enough for me.
		iterations = 100
		#print("You've selected 0 or fewer iterations; nothing will happen.")
	translatedText = asyncio.run(translateText(inputText, iterations, langCode))
	print("Original text:", inputText)
	print("Translated text:", translatedText)
	if platform.system().lower() != "linux":
		pyperclip.copy(translatedText)
		print("Copied result to clipboard.")
	else:
		print("Copying doesnt work on linux sorry =(")

async def langDetect(detectThis):
	async with Translator() as translator:	
		tmp = await translator.detect(detectThis) 
		return tmp.lang

if __name__ == "__main__":
	while True:
		main()
		yn = input('Done. Try another word? (y/n) ').strip().lower()
		if yn == 'y' or yn == 'yes':
			continue
		elif yn == 'n' or yn == 'no':
			print('Exiting now...')
			if ghVer < ver1:
				print("Now get back in your DeLorean")
			break
		else:
			break
