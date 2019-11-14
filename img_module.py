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
	th = gray_img.point(lambda x: 0 if x < 93 else 255)

	op = img_opening(th, 5)

	cl = img_closing(th, 1)

	th = cl

	th = th.crop((0, 0, gray_img.width, int(gray_img.height / 2) ))

	th = th.convert("RGB")

	pos = ocr_module.target_to_ocr(th)

	#ブラウザに一旦、切り出した画像を返す → タイトル領域を選ばせる

	img_arr = []
	cnt = 0;

	for iter in pos:
		#抽出文字列長が短いときはノイズとして除外する
		if len(iter.content) > 5:
			x_st = iter.position[0][0]
			y_st = iter.position[0][1]
			x_en = iter.position[1][0]
			y_en = iter.position[1][1]
			im_cut = th.crop((x_st, y_st, x_en, y_en))
			print(cnt, ":" ,iter.content)
			#im_cut.show()
			cnt = cnt + 1
			img_arr.append(im_cut)

	print("どの画像を表示するか?")
	i = input()
	img_arr[int(i)].show()
	"""
	x_st = pos[3].position[0][0]
	y_st = pos[3].position[0][1]
	x_en = pos[3].position[1][0]
	y_en = pos[3].position[1][1]

	print(pos[3].position[0][0])
	print(pos[3].content)


	x_st = gray_img.width / 20
	y_st = gray_img.height / 20
	x_en = gray_img.width - x_st
	y_en = gray_img.height - y_st

	im_cut = th.crop((x_st, y_st, x_en, y_en))
	#im_cut.show()

	"""
