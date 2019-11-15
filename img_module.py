from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import ocr_module

#指定回数膨張させる(白領域を増やす)
def img_opening(img, n):
	img_op = img
	for i in range(n):
		img_op = img_op.filter(ImageFilter.MaxFilter())
	return img_op

#指定回数縮小させる(黒領域を増やす)
def img_closing(img, n):
	img_cl = img
	for i in range(n):
		img_cl = img_cl.filter(ImageFilter.MinFilter())
	return img_cl

def img_to_gray(target):
	img = Image.open(target)
	gray_img = img.convert("L")
	gray_img.show()

def show_img_histogram(img):
	plt.plot(img.histogram())
	plt.show()

def ticket_threshold(target):
	img = Image.open(target)
	gray_img = img.convert("L")

	gray_img = gray_img.resize( (int(gray_img.width / 2), int(gray_img.height / 2) ) )
	#gray_img.show()

	#ラムダ式で2値化 画像は0(黒)～255(白)
	#黒が濃い(文字の印字)部分を残し、それ以外を白く飛ばす
	bin_img = gray_img.point(lambda x: 0 if x < 93 else 255)

	pre_img = bin_img

	#pre_img = img_opening(pre_img, 1)

	#pre_img = img_closing(pre_img, 1)


	rem_noise_img = pre_img

	rem_noise_img = rem_noise_img.crop((0, 0, gray_img.width, int(gray_img.height / 2) ))
	rem_noise_img.show()
	rem_noise_img = rem_noise_img.convert("RGB")

	pos = ocr_module.target_to_ocr(rem_noise_img)

	#ブラウザに一旦、切り出した画像を返す → タイトル領域を選ばせる

	area_point_arr = []
	cnt = 0;

	for iter in pos:
		#抽出文字列長が短いときはノイズとして除外する
		if len(iter.content) > 5:
			x_st = iter.position[0][0]
			y_st = iter.position[0][1]
			x_en = iter.position[1][0]
			y_en = iter.position[1][1]
			im_cut = rem_noise_img.crop((x_st, y_st, x_en, y_en))
			print(cnt, ":" ,iter.content)

			cnt = cnt + 1
			#img_arr.append(im_cut)
			area_point_arr.append([x_st, y_st, x_en, y_en])

	if len(area_point_arr) < 1:
		print("抽出できません")
		exit()

	print("どの画像を表示するか?")
	i = input()
	return area_point_arr[int(i)]

#取得した領域に対してOCRする処理
def area_img_to_ocr(target, position):
	img = Image.open(target)
	gray_img = img.convert("L")
	cut_img = gray_img.crop(position)
	cut_img.show()

	"""
	title_area_ocr_wrapper(img)

	pre_img = img.resize( (img.width + 10, img.height + 10) )

	title_area_ocr_wrapper(pre_img)

	"""
	#pre_img = img_closing(pre_img, 1)
	#title_area_ocr_wrapper(pre_img)

#タイトル領域に対してOCRして結果を取得する処理 (debug用)
def title_area_ocr_wrapper(img):
	pos = ocr_module.target_to_ocr(img)

	if len(pos) < 1:
		print("抽出できません")
		exit()

	for iter in pos:
		print(iter.content)
