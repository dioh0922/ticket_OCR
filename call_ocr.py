import sys
import io
import os

from PIL import Image
import pyocr
import pyocr.builders

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, "UTF-8")

args = sys.argv

#引数チェック ファイル名を指定する
if 2 > len(args):
	print("引数が少なすぎます")
	exit(1)
if os.path.isfile(args[1]) == 0:
	print("ファイルがありません")
	exit(1)

target = args[1]

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
