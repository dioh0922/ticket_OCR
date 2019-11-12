from PIL import Image
from PIL import ImageDraw
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

			"""
			t = tool[0].image_to_string(image,
				lang="jpn",
				builder=pyocr.builders.TextBuilder(tesseract_layout=6)
				)

			print(t)
			"""
			box = tool[0].image_to_string(image,
				lang="jpn",
				builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6)
				)

			#描画処理用のインスタンスに矩形を描画
			pos_img = ImageDraw.Draw(image)

			for pos in box:
				print("w:{}, pos:{}".format(pos.content, pos.position))
				pos_img.rectangle(pos.position, outline="red", width=3)

			#処理結果を表示(描画オブジェクトで書き込まれるのは元のオブジェクト)
			image.show()

		except Exception as e:
			print(e)
