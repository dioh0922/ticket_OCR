import os
import random
import numpy as np
import jaconv
import txt_module

"""
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
"""

#与えた文字列を結果ファイルに追記する処理
def add_to_resultflie(txt):
	file = open("test_train.txt", "a", encoding = "utf-8")
	file.write(txt)
	file.write("\n")
	file.close()

	return 0

#ランダムに並べ替えて訓練用の文字列に変換する処理
def create_shuffle_txt(title_list, kana_list):

	#半角濁音は文章に混ぜるため配列の前から90%の位置までの範囲に入れるように乱数を発生させる
	offset = int(len(title_list) / 10)
	arr = np.random.randint(0, len(title_list) - offset, (1, 50))

	ins_arr = np.sort(arr)

	ins_iter = 0
	daku_iter = 0
	out_str = ""

	idx = 0

	#乱数で設定したtrain_listの位置に半角濁音を入れる
	for i in range(len(title_list)):
		out_str += title_list[i]
		if i == int(ins_arr[0][ins_iter]):
			ins_iter += 1

			#先頭に戻すが以降はtrain_listと一致しないので参照しない
			if ins_iter == 50:
				ins_iter = 0

			if idx < len(kana_list):
				out_str += jaconv.z2h(kana_list[idx], kana = True)
				idx += 1

		if (i + 1) % 30 == 0:
			out_str += "\n"

	add_to_resultflie(out_str)

	return 0

#渡した配列を文字列にする処理
def transform_list_to_str(list):
	result = ""
	for i in range(len(list)):
		result += list[i]
		if (i + 1) % 30 == 0:
			result += "\n"
	return result

#訓練用のテキストを取得する処理
def get_train_title_data():
	result_list = []
	file = open("./train_txt/train_movie.txt", "r", encoding="utf-8")
	read_list = file.read()
	file.close()

	for i in read_list:
		result_list += i.rstrip("\n")

	return result_list

def get_train_kana_data():
	result_list = []
	file = open("./train_txt/train_kana.txt", "r", encoding = "utf-8")
	read_list = file.read()
	file.close()

	for i in read_list:
		result_list += i.rstrip("\n")

	return result_list

#半角カナ濁音のテキストを取得する処理
def get_dakuon_data():
	file = open("./train_txt/train_dakuon_zen.txt", "r", encoding = "utf-8")
	read_list = file.read()
	file.close()

	result_list = []
	for i in read_list:
		result_list += i.rstrip("\n")

	return result_list

#訓練用のテキストを生成し出力する処理
def create_train_txt():
	"""
	1.サンプルの文章を読み取り、文字ごとに乱数で順番を入れ替える(改行は取る)
	2.半角濁点用のファイルを読み取り、改行を取る
	3.半角濁点の要素を指すインデックスの配列を作り
	  乱数で入れ替える(2文字で1つのため増分2で参照していく)
	4.文章配列の長さの範囲で乱数の配列を生成する(該当位置に半角濁点を差し込む)
	5.文章配列を参照しながら半角濁点を差し込み、ファイル出力する(一定間隔で改行する)
	"""

	title_list = []	#半角カナのため濁音は2文字
	title_list = get_train_title_data()
	title_list += get_train_kana_data()
	random.shuffle(title_list)

	kana_list = []
	kana_list = get_dakuon_data()
	random.shuffle(kana_list)

	create_shuffle_txt(title_list, kana_list)

	return 0

def add_row_teachdata():
	title_list = []

	title_list = get_train_title_data()

	row_order = transform_list_to_str(title_list)

	add_to_resultflie(row_order)

	return 0

#半角カナを追加で半角スペース区切りと1文字改行で追加する
def add_kana_reinforce():
	kana_list = []
	kana_str = ""

	file = open("./train_txt/train_kana.txt", "r", encoding = "utf-8")
	read_list = file.read()
	file.close()

	for i in read_list:
		kana_list += i.rstrip("\n")

	#1文字ずつスペースで区切る
	for i in range(len(kana_list)):
		kana_str += kana_list[i]
		kana_str += " "
		if (i + 1) % 30 == 0:
			kana_str += "\n"

	kana_str += "\n"

	#1文字ずつ改行する
	for i in range(len(kana_list)):
		kana_str += kana_list[i]
		kana_str += "\n"

	add_to_resultflie(kana_str)

	return 0

#半角カナの濁音を追加する処理
def add_kana_daku_reinforce():
	add_str = ""
	kana_list = []

	kana_list = get_dakuon_data()

	for i in range(len(kana_list)):
		add_str += jaconv.z2h(kana_list[i], kana = True)
		if (i + 1) % 15 == 0:
			add_str += "\n"

	add_str += "\n"

	for i in range(len(kana_list)):
		add_str += jaconv.z2h(kana_list[i], kana = True)
		add_str += " "
		if (i + 1) % 15 == 0:
			add_str += "\n"

	for i in range(len(kana_list)):
		add_str += jaconv.z2h(kana_list[i], kana = True)
		add_str += "\n"

	add_to_resultflie(add_str)

	return 0

#元のタイトルを半角に変換して追記する処理
def add_trans_hankaku():
	title_list = []
	title_list = get_train_title_data()

	add_str = transform_list_to_str(title_list)
	save_str = jaconv.z2h(add_str, kana = True, digit = True)
	add_to_resultflie(save_str)

	random.shuffle(title_list)
	add_str = transform_list_to_str(title_list)
	save_str = jaconv.z2h(add_str, kana = True, digit = True)
	add_to_resultflie(save_str)

	return 0
