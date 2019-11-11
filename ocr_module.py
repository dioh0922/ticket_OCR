from PIL import Image
import pyocr
import pyocr.builders
import os

def ocr(target):
	if os.path.isfile(target) == 0:
		print("ファイルがありません")
		exit(1)

	tool = pyocr.get_available_tools()
	if len(tool) == 0:
		print("No OCR")
		exit(1)
	else:
		try:
			image = Image.open(target)
			t = tool[0].image_to_string(image,
				lang="jpn",
				builder=pyocr.builders.TextBuilder(tesseract_layout=6)
				)

			print(t)

		except Exception as e:
			print(e)
