import os
import random
import numpy as np
import jaconv
import wikipedia
import time
import revision_module
from concurrent.futures import ThreadPoolExecutor

TRAIN_TXT = "test_train.txt"
UTF8 = "utf-8"

#テキスト補正処理のラッパー関数
def revision_txt(row_txt):
	proc_txt = jaconv.z2h(row_txt, digit=True)
	#半角を全角にした後に登録したパターンで補正する
	return revision_module.revision_from_dictionary(jaconv.h2z(proc_txt, kana=True))

#識別結果を補正し確認する処理
def print_detect_word(txt):
	print("補正前:",txt)
	print("補正後:",revision_txt(txt))

#与えた文字列を結果ファイルに追記する処理
def add_to_resultflie(txt):
	file = open(TRAIN_TXT, "a", encoding = UTF8)
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
	return get_target_txt("./train_txt/train_movie.txt", UTF8)

#訓練用のカナ文字列を取得する処理
def get_train_kana_data():
	return get_target_txt("./train_txt/train_kana.txt", UTF8)

#半角カナ濁音のテキストを取得する処理
def get_dakuon_data():

	read_list = get_target_txt("./train_txt/train_dakuon_zen.txt", UTF8)

	result_list = []
	for i in read_list:
		result_list += i.rstrip("\n")

	return result_list

#訓練用のテキストを生成し出力する処理
def create_train_txt():

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

	#jpn48では元の並び順はここでは追記しないためコメントアウト
	#row_order = "".join(get_list)
	#add_to_resultflie(row_order)


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

	read_list = get_target_txt("./train_txt/train_kana.txt", UTF8)

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

	read_list += get_target_txt("./train_txt/train_specifies.txt", UTF8)
	#read_list += get_target_txt("./train_txt/wiki_page_content.txt", "utf-8")

	for i in read_list:
		spec_list += i

	add_str = "".join(spec_list)
	add_to_resultflie(add_str)

	wiki_content = get_wiki_content_txt()
	train_str = "".join(wiki_content)
	add_to_resultflie(train_str)

	add_to_resultflie(jaconv.z2h(add_str, kana = True, digit = True))

	add_to_resultflie(jaconv.z2h(train_str, kana = True, digit = True))

	return 0

#元のOCRでの訓練用テキストの取得処理
def get_default_train_txt():
	return get_target_txt("./train_txt/jpn_train.txt", UTF8)

#元の訓練テキストを処理して追記する処理
def add_default_train_txt():
	train_list = get_default_train_txt()
	train_str = "".join(train_list)
	add_to_resultflie(train_str)
	add_to_resultflie(jaconv.z2h(train_str, kana = True, digit = True))
	return 0

#wikipediaAPIで記事から訓練用テキストを生成する
def train_txt_crawling():

	file = open("./train_txt/get_wiki_list.txt", "r", encoding = UTF8)
	read_list = file.readlines()
	file.close()

	txt = ""
	str = ""

	executor = ThreadPoolExecutor(max_workers=15)
	get_pages = []

	st = time.time()

	for i in read_list:
		#print(i.rstrip("\n"),"の取得完了")
		future = executor.submit(send_wiki_page_request, i)
		get_pages.append(future)

	for i in get_pages:
		str += i.result()

	executor.shutdown()

	now = time.time()

	print("%#.2f秒かかりました" % (now - st) )

	for i in range(len(str)):
		txt += str[i].rstrip("\n")
		if (i + 1) % 30 == 0:
			txt += "\n"

	file = open("./train_txt/wiki_page_content.txt", "a", encoding = UTF8)
	file.write(txt)
	file.write("\n")
	file.close()

	return 0

#wikipediaから記事を取得する処理
def send_wiki_page_request(target):
	str = ""
	wikipedia.set_lang("ja")
	response = wikipedia.search(target)
	if len(response) > 0:
		content = wikipedia.page(response[0])
		str += content.content[0:150]
	#取得する文字数が大きくなる=>ファイルが1000kB程度で過学習っぽい結果になる
	return str

#事前に取得したwikipediaの記事のファイルを読み出すラッパー
def get_wiki_content_txt():
	return get_target_txt("./train_txt/wiki_page_content.txt", UTF8)

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
