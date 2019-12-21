import sys
import io
import os
import glob
from PIL import Image

import ocr_module
import img_module
import txt_module

result_list = glob.glob("./get_result/" + "*")
for i in result_list:
	os.remove(i)

img_list = glob.glob("./area/" + "*")

if len(img_list) <= 0 :
	exit()

print("どの画像を表示するか?")
i = input()

target_img = "./area/" + i + ".jpg"

gray_img = img_module.img_proc_filter(target_img)

detect_list = ocr_module.test_trained_ocr(gray_img)

for txt in detect_list:
	txt_module.print_detect_word(txt.content)


#img_module.area_img_to_ocr(args[1], detected_area)
#OCR処理で画像を取得しておき、画像を全て表示してみる
img_list = glob.glob("./get_result/" + "*")

for i in img_list:
	img = Image.open(i)
	img.show()
