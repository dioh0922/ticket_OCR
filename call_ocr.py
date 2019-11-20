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

if 3 <= len(args):
	if args[2] == "-t":
		img_module.test_trained_model(args[1])

	elif args[2] == "-c":
		detected_area = img_module.ticket_threshold(args[1])
		img_module.cut_title_area(args[1], detected_area)

	elif args[2] == "-h":
		print("-t: 訓練モデル全てでタイトル画像にOCR")
		print("-c: タイトル領域を切り出す(直下にtmp.jpg)")
		print("-d: 2値画像を表示する")

	elif args[2] == "-d":
		img_filter = img_module.img_proc_filter(args[1])
		img_filter.show()
		print(img_filter.width)
		print(img_filter.height)

	elif args[2] == "-s":
		img_module.test_default_model(args[1])

	else:
		print("error debug option")
	exit()
#ocr_module.ocr(args[1])
#img_module.img_to_gray(args[1])

#指定した画像からタイトル領域を取得する
detected_area = img_module.ticket_threshold(args[1])

img_module.area_img_to_ocr(args[1], detected_area)

print("処理が終わりました")
