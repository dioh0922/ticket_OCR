import sys
import io

import ocr_module
import img_module

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, "UTF-8")

args = sys.argv

#引数チェック ファイル名を指定する
if 2 > len(args):
	print("引数が少なすぎます")
	exit(1)

#ocr_module.ocr(args[1])
#img_module.img_to_gray(args[1])

#指定した画像からタイトル領域を取得する
detected_area = img_module.ticket_threshold(args[1])
print(detected_area)
img_module.area_img_to_ocr(args[1], detected_area)
