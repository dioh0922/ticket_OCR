import os
import random
import numpy as np
import jaconv
import wikipedia
from concurrent.futures import ThreadPoolExecutor

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

#一定間隔ごとに開業コードを挿入する処理
def insert_CRLF(list):
	result = []
	for i in range(len(list)):
		result += list[i].rstrip("\n")
		if (i + 1) % 30 == 0:
			result += "\n"
	return result

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

#訓練用のテキストを取得する処理
def get_train_title_data():
	return get_target_txt("./train_txt/train_movie.txt", "utf-8")

#訓練用のカナ文字列を取得する処理
def get_train_kana_data():
	return get_target_txt("./train_txt/train_kana.txt", "utf-8")

#半角カナ濁音のテキストを取得する処理
def get_dakuon_data():

	read_list = get_target_txt("./train_txt/train_dakuon_zen.txt", "utf-8")

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

	train_list = []	#半角カナのため濁音は2文字

	get_list = get_train_title_data()
	get_list += get_train_kana_data()

	for i in get_list:
		train_list += i.rstrip("\n")

	random.shuffle(train_list)

	kana_list = []
	kana_list = get_dakuon_data()
	random.shuffle(kana_list)

	create_shuffle_txt(train_list, kana_list)

	return 0

#入れ替えずに連結して追記する処理
def add_row_teachdata():
	title_list = []
	train_str = ""
	get_list = get_train_title_data()

	title_list = insert_CRLF(get_list)

	row_order = "".join(title_list)
	add_to_resultflie(row_order)
	return 0

#半角カナを追加で半角スペース区切りと1文字改行で追加する
def add_kana_reinforce():
	kana_list = []
	kana_str = ""

	read_list = get_target_txt("./train_txt/train_kana.txt", "utf-8")

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
	train_list = []
	get_list = get_train_title_data()

	#初めは順番そのままで変換して追記する
	train_list = insert_CRLF(get_list)
	add_str = "".join(train_list)
	add_to_resultflie(jaconv.z2h(add_str, kana = True, digit = True))

	#そのあとに順番を入れ替えて変換して追記する
	train_list = trans_order_list(train_list)
	add_str = "".join(train_list)
	add_to_resultflie(jaconv.z2h(add_str, kana = True, digit = True))

	return 0

#タイトルを改行して列挙する
def add_specifies():
	spec_list = []

	read_list = get_train_title_data()

	for i in read_list:
		spec_list += i

	read_list = get_target_txt("./train_txt/train_specifies.txt", "utf-8")
	#read_list += get_target_txt("./train_txt/wiki_page_content.txt", "utf-8")

	for i in read_list:
		spec_list += i

	add_str = "".join(spec_list)
	add_to_resultflie(add_str)
	add_to_resultflie(jaconv.z2h(add_str, kana = True, digit = True))

	add_wiki_content()

	return 0

#元のOCRでの訓練用テキストの取得処理
def get_default_train_txt():
	return get_target_txt("./train_txt/jpn_train.txt", "utf-8")

#元の訓練テキストを処理して追記する処理
def add_default_train_txt():
	train_list = get_default_train_txt()
	train_str = "".join(train_list)
	add_to_resultflie(train_str)
	add_to_resultflie(jaconv.z2h(train_str, kana = True, digit = True))
	return 0

#wikipediaAPIで記事から訓練用テキストを生成する
def train_txt_mining():

	file = open("./train_txt/get_wiki_list.txt", "r", encoding = "utf-8")
	read_list = file.readlines()
	file.close()

	txt = ""
	str = ""

	executor = ThreadPoolExecutor(max_workers=10)
	get_pages = []

	for i in read_list:
		print(i.rstrip("\n"),"の取得完了")
		future = executor.submit(send_wiki_page_request, i)
		get_pages.append(future)

	for i in get_pages:
		str += i.result()

	executor.shutdown()

	for i in range(len(str)):
		txt += str[i].rstrip("\n")
		if (i + 1) % 30 == 0:
			txt += "\n"

	file = open("./train_txt/wiki_page_content.txt", "a", encoding = "utf-8")
	file.write(txt)
	file.write("\n")
	file.close()

	return 0

def send_wiki_page_request(target):
	str = ""
	wikipedia.set_lang("ja")
	response = wikipedia.search(target)
	content = wikipedia.page(response[0])
	str += content.content[0:300]
	return str

#事前に取得したwikipediaの記事のファイルを読み出すラッパー
def get_wiki_content_txt():
	return get_target_txt("./train_txt/wiki_page_content.txt", "utf-8")

#事前に取得したwikipediaの記事を追記する処理
def add_wiki_content():
	wiki_content = get_wiki_content_txt()
	train_str = "".join(wiki_content)
	add_to_resultflie(train_str)
	add_to_resultflie(jaconv.z2h(train_str, kana = True, digit = True))

	add_wiki_content_trans()

	return 0

#取得しておいた記事の文字列を並べ替えて追記する処理
def add_wiki_content_trans():
	wiki_content = get_wiki_content_txt()
	train_list = []

	train_list = trans_order_list(wiki_content)

	str = "".join(train_list)
	add_to_resultflie(str)
	add_to_resultflie(jaconv.z2h(str, kana = True, digit = True))

	return 0

#指定したファイルを指定した文字コードで取得する関数
def get_target_txt(target, encoding):
	file = open(target, "r", encoding = encoding)
	read_list = file.read()
	file.close()

	return read_list

#順番を入れ替えた配列に変換する処理
def trans_order_list(list):
	trans_list = []

	for i in list:
		trans_list += i.rstrip("\n")

	random.shuffle(trans_list)
	trans_list = insert_CRLF(trans_list)

	return trans_list
