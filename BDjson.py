import asyncio, pyperclip, json
from googletrans import Translator, LANGUAGES
from tqdm import tqdm
from time import sleep
from random import choice

async def main():
	#parse json
	jsonFile = input('Name of the json file: ')
	##print(jsonFile)
	with open(jsonFile, 'r', encoding='utf-8') as f:
		jsonContent = json.load(f)
	for i in tqdm(jsonContent):
		async with Translator() as translator:	
			detection = await Translator().detect(i)
		


async def translateText(text, iterations, langCode):
	translator = Translator()
	resultTrans = text
	for i in tqdm(range(iterations), desc="Translating" , bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt} | {elapsed} elapsed | ETA: {remaining}"):
		try:
			while True:
				randomLang = choice(list(LANGUAGES))
				if randomLang != langCode:
					break
			randomTrans = await translator.translate(resultTrans, dest=randomLang)
			resultTrans = await translator.translate(randomTrans.text, dest=langCode)
			resultTrans = resultTrans.text
			tqdm.write(f"Iteration {i + 1}/{iterations} ({LANGUAGES[randomLang]} to {LANGUAGES[langCode]}): {resultTrans}")
		except Exception as e:
			tqdm.write(f"Error during translation at iteration {i + 1}: {e}")
			sleep(1)
	return resultTrans

	

if __name__ == "__main__":
	while True:
		asyncio.run(main())
		yn = input('Done.\nTry another file? (y/n) ').strip().lower()
		if yn == 'y' or yn == 'yes':
			continue
		elif yn == 'n' or yn == 'no':
			print('Exiting now...')
			#if ghVer < ver1:
			#	print("Now get back in your DeLorean")
			#	break
		else:
			break