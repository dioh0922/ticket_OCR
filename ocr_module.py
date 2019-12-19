from PIL import Image
from PIL import ImageDraw
import pyocr
import pyocr.builders
import os
import glob
from icrawler.builtin import GoogleImageCrawler
import txt_module

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

#識別する言語を指定して画像にOCRする処理
def ocr_to_target_lang(img, language):
	tool = pyocr.get_available_tools()
	if len(tool) == 0:
		print("No OCR")
		exit(1)
	try:
		#タイトルでひとまとまりのため行単位で取得する
		box = tool[0].image_to_string(img,
			lang=language,
			builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6)
			)

		return box

	except Exception as e:
		print(e)

#訓練した教師データでテストする処理
def test_trained_ocr(img):

	train = "jpn48"

	list = ocr_to_target_lang(img, train)

	return list

#サンプルのモデルでOCRするラッパー
def test_default_model_ocr(img):
	test_target_ocr(img, "jpn")

#指定した言語モデルでOCRする処理
def test_target_ocr(img, target):
	print(target)
	ocr_to_target_lang(img, target)
