from PIL import Image
from PIL import ImageDraw
import pyocr
import pyocr.builders
import os

#画像データ自体を渡してOCRする
def target_to_ocr(img):
	tool = pyocr.get_available_tools()
	if len(tool) == 0:
		print("No OCR")
		exit(1)
	try:
		box = tool[0].image_to_string(img,
			lang="jpn",
			builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6)
			)

		return box

	except Exception as e:
		print(e)

#元の画像に抽出領域を描画する処理
def ocr_draw_rectangle(img):
	tool = pyocr.get_available_tools()
	if len(tool) == 0:
		print("No OCR")
		exit(1)
	try:
		box = tool[0].image_to_string(img,
			lang="jpn",
			builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6)
			)

		#描画処理用のインスタンスに矩形を描画
		pos_img = ImageDraw.Draw(img)

		for pos in box:
			#print("w:{}, pos:{}".format(pos.content, pos.position))
			pos_img.rectangle(pos.position, outline="red", width=3)

		#処理結果を表示(描画オブジェクトで書き込まれるのは元のオブジェクト)
		img.show()


		return box

	except Exception as e:
		print(e)
