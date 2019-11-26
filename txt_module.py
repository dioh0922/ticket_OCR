import os
import random
import numpy as np
import jaconv
import txt_module


#文字列中の濁点、半濁点を1文字に統合する処理
def txt_dakuten_marge(txt):
	tmp_txt = txt
	for word in tmp_txt:
		print(word)
	return 0

#濁点を発見したら1文字に変換させる処理
def dakuon_exchange(word):
	if word == "カ":
		result = "ガ"
	else:
		result = word
	return result

def create_shuffle_txt(title_list, kana_list, kana_idx):
	random.shuffle(kana_idx)
	idx = kana_idx[0]

	#半角濁音は文章に混ぜるため配列の前から90%の位置までの範囲に入れるように乱数を発生させる
	offset = int(len(title_list) / 10)
	arr = np.random.randint(0, len(title_list) - offset, (1, 50))

	ins_arr = np.sort(arr)

	ins_iter = 0
	daku_iter = 0
	out_str = ""

	#乱数で設定したtrain_listの位置に半角濁音を入れる
	for i in range(len(title_list)):
		out_str += title_list[i]
		if i == int(ins_arr[0][ins_iter]):
			ins_iter += 1

			#先頭に戻すが以降はtrain_listと一致しないので参照しない
			if ins_iter == 50:
				ins_iter = 0

			if daku_iter < len(kana_list):
				idx = kana_idx[int(daku_iter / 2)]
				out_str += kana_list[idx]
				out_str += kana_list[idx + 1]
				daku_iter += 2

		if (i + 1) % 30 == 0:
			out_str += "\n"

	file = open("test_train.txt", "a", encoding = "utf-8")
	file.write(out_str)
	file.write("\n")
	file.close()


def create_train_txt():
	"""
	1.サンプルの文章を読み取り、単語ごとに乱数で順番を入れ替える(改行は取る)
	2.半角濁点用のファイルを読み取り、改行を取る
	3.半角濁点の要素を指すインデックスの配列を作り
	  乱数で入れ替える(2文字で1つのため増分2で参照していく)
	4.文章配列の長さの範囲で乱数の配列を生成する(該当位置に半角濁点を差し込む)
	5.文章配列を参照しながら半角濁点を差し込み、ファイル出力する(一定間隔で改行する)
	"""

	title_list = []	#半角カナのため濁音は2文字

	file = open("./train_txt/train_movie.txt", "r", encoding="utf-8")
	read_list = file.read()
	file.close()

	for i in read_list:
		title_list += i.rstrip("\n")

	file = open("./train_txt/train_kana.txt", "r", encoding = "utf-8")
	read_list = file.read()
	file.close()

	for i in read_list:
		title_list += i.rstrip("\n")

	random.shuffle(title_list)

	file = open("./train_txt/train_dakuon.txt", "r", encoding = "utf-8")
	read_list = file.read()
	file.close()

	kana_list = []
	for i in read_list:
		kana_list += i.rstrip("\n")

	kana_idx = []
	for cnt in range(0, len(kana_list), 2):
		kana_idx.append((cnt))

	create_shuffle_txt(title_list, kana_list, kana_idx)
