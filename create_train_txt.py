"""
1.サンプルの文章を読み取り、単語ごとに乱数で順番を入れ替える(改行は取る)
2.半角濁点用のファイルを読み取り、改行を取る
3.半角濁点の要素を指すインデックスの配列を作り
  乱数で入れ替える(2文字で1つのため増分2で参照していく)
4.文章配列の長さの範囲で乱数の配列を生成する(該当位置に半角濁点を差し込む)
5.文章配列を参照しながら半角濁点を差し込み、ファイル出力する(一定間隔で改行する)
"""


import os
import random
import numpy as np
import jaconv
import txt_module

train_list = []	#半角カナのため濁音は2文字

file = open("./train_txt/train_movie.txt", "r", encoding="utf-8")
read_list = file.read()
file.close()

for i in read_list:
	train_list += i.rstrip("\n")

file = open("./train_txt/train_kana.txt", "r", encoding = "utf-8")
read_list = file.read()
file.close()

for i in read_list:
	train_list += i.rstrip("\n")

random.shuffle(train_list)

file = open("./train_txt/train_dakuon.txt", "r", encoding = "utf-8")
read_list = file.read()
file.close()

daku_list = []
for i in read_list:
	daku_list += i.rstrip("\n")

dakuten_idx = []
for cnt in range(0, len(daku_list), 2):
	dakuten_idx.append((cnt))

random.shuffle(dakuten_idx)
idx = dakuten_idx[0]

"""
train_list => 映画タイトル
daku_list => 半角濁点
dakuten_idx => 半角の要素を指す(乱数)
ins_arr => train_listのどこに半角入れるか(インデックスを乱数で持つ)
"""

arr = np.random.randint(0, len(train_list) - 1, (1, 50))

ins_arr = np.sort(arr)

ins_iter = 0
daku_iter = 0
out_str = ""

#乱数で設定したtrain_listの位置に半角濁音を入れる
for i in range(len(train_list)):
	out_str += train_list[i]
	if i == int(ins_arr[0][ins_iter]):
		print(i, ":", int(ins_arr[0][ins_iter]))
		ins_iter += 1

		#先頭に戻すが以降はtrain_listと一致しないので参照しない
		if ins_iter == 50:
			ins_iter = 0

		if daku_iter < len(dakuten_idx):
			idx = dakuten_idx[daku_iter]
			out_str += daku_list[idx]
			out_str += daku_list[idx + 1]
			daku_iter += 2
			print(daku_iter)

	if i % 20 == 0:
		out_str += "\n"

file = open("test_train.txt", "w", encoding = "utf-8")
file.write(out_str)
file.close()
#print(len(iter_list))
