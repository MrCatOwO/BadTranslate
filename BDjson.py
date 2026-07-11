import asyncio, json
from googletrans import Translator, LANGUAGES
from tqdm.asyncio import tqdm
from time import perf_counter
from random import choice
from os.path import exists
from os import remove, environ

async def main():
	tmpDir = environ.get("TEMP")
	start = perf_counter()
	#parse json
	jsonFile = input("Name of the json file: ")
	iterations = input("Iterations: ")
	#iterations = 100
	#jsonFile = "en_us.json"
	if exists(f"{tmpDir}\\BDjsonTmpSave.json"):
		with open(f"{tmpDir}\\BDjsonTmpSave.json", "r", encoding="utf-8") as f:
			jsonContent = json.load(f)
		with open(f"{tmpDir}\\pos.txt", "r", encoding="utf-8") as f:
			startingPos = int(f.read())
	else:
		with open(jsonFile, "r", encoding="utf-8") as f:
			jsonContent = json.load(f)
			startingPos = 0
	keys = list(jsonContent.keys())
	async with Translator() as translator:
		print(type(jsonContent))
		for i in tqdm(range(startingPos, len(jsonContent))):
			tqdm.write(jsonContent[keys[i]])
			with open(f"{tmpDir}\\pos.txt", "w", encoding="utf-8") as f:
				f.write(str(i))
			"""try:
				detection = await translator.detect(jsonContent[keys[i]])
				detection = detection.lang
			except Exception as e:
				print(f"Detetion error: {e}.\nFalling back to english")"""
			detection = "en"
			jsonContent[keys[i]] = await translateText(jsonContent[keys[i]], iterations, detection, translator)
			print(jsonContent[keys[i]])
			with open(f"{tmpDir}\\BDjsonTmpSave.json", "w", encoding="utf-8") as f:
				json.dump(jsonContent, f, ensure_ascii=False)
	with open("out.json", "w", encoding="utf-8") as f:
		json.dump(jsonContent, f, ensure_ascii=False)
	try:
		remove(f"{tmpDir}\\BDjsonTmpSave.json")
		
	except FileNotFoundError:
		pass
	try:
		remove(f"{tmpDir}\\pos.txt")
	except FileNotFoundError:
		pass
	print(f"Total translation time: {start - perf_counter():.2f} s")

async def translateText(text, iterations, langCode, translator):
	resultTrans = text
	for i in tqdm(range(iterations)):
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
			await asyncio.sleep(7.5)
	return resultTrans



if __name__ == "__main__":
	while True:
		asyncio.run(main())
		yn = input("Done.\nTry another file? (y/n) ").strip().lower()
		if yn == "y" or yn == "yes":
			continue
		elif yn == "n" or yn == "no":
			print("Exiting now...")
			#if ghVer < ver1:
			#	print("Now get back in your DeLorean")
			break
		else:
			break