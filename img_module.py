from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import ocr_module

def img_to_gray(target):
	img = Image.open(target)
	gray_img = img.convert("L")
	gray_img.show()

def ticket_threshold(target):
	img = Image.open(target)
	gray_img = img.convert("L")

	#gray_img.show()
	#plt.plot(gray_img.histogram())
	#plt.show()

	#ラムダ式で2値化 画像は0(黒)～255(白)
	#黒が濃い(文字の印字)部分を残し、それ以外を白く飛ばす
	th = gray_img.point(lambda x: 0 if x < 100 else 255)
	th = th.filter(ImageFilter.MaxFilter())
	th = th.filter(ImageFilter.MinFilter())
	th = th.filter(ImageFilter.MinFilter())

	th = th.convert("RGB")
	th.show()
	ocr_module.target_to_ocr(th)
