import sys
import io
import os
import glob
from PIL import Image

import ocr_module
import img_module
import txt_module

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, "UTF-8")

args = sys.argv

#引数チェック ファイル名を指定する
if 2 > len(args):
	print("引数が少なすぎます")
	exit()
elif args[1] == "-create":
	txt_module.create_train_txt()
	print("訓練用のテキストを作成しました")
	txt_module.add_to_resultflie("-create")
	exit()
elif args[1] == "-kana":
	txt_module.add_kana_reinforce()
	print("半角カナの追記をしました")
	txt_module.add_to_resultflie("-kana")
	exit()
elif args[1] == "-daku":
	txt_module.add_kana_daku_reinforce()
	print("半角カナ濁音の追記をしました")
	txt_module.add_to_resultflie("-daku")
	exit()
elif args[1] == "-row":
	txt_module.add_row_teachdata()
	print("順番を入れ替えずに訓練用のテキストを作成しました")
	txt_module.add_to_resultflie("-row")
	exit()
elif args[1] == "-trans":
	txt_module.add_trans_hankaku()
	print("元のタイトルを半角に変換して追記しました")
	txt_module.add_to_resultflie("-trans")
	exit()
elif args[1] == "-spec":
	txt_module.add_specifies()
	print("指定した単語を追記しました")
	txt_module.add_to_resultflie("-spec")
	exit()
elif args[1] == "-default":
	txt_module.add_default_train_txt()
	print("元の訓練テキストを追記しました")
	exit()
elif args[1] == "-crawling":
	txt_module.train_txt_crawling()
	print("Wikipediaから記事を取得しました")
	exit()
elif args[1] == "-wiki":
	txt_module.add_wiki_content()
	print("Wikipediaの記事を訓練テキストに追記しました")
	exit()
elif args[1] == "-rev":
	print(txt_module.revision_txt("4DX ｶﾞ -ﾙス筈 ＆パ ンツァー1+2話"))
	exit()
elif args[1] == "-h":
	print("-create: 訓練用のテキストを作成する")
	print("-kana: 半角カナ(1文字)を追加で訓練データにする")
	print("-row: タイトルなどのデータを入れ替えずに訓練データにする")
	print("-daku: 半角カナ濁音を追加で訓練データにする")
	print("-trans: タイトルの文字列を半角に変換して記録する")
	print("-spec: wikiや事前に決めた単語を追記する")
	exit()

if 3 <= len(args):
	if args[2] == "-t":
		#前の検索結果を消しておく(本番環境ではAPI側で先に消す)
		img_list = glob.glob("./get_result/" + "*")
		for i in img_list:
			os.remove(i)

		gray_img = img_module.img_proc_filter(args[1])

		gray_img.show()

		detect_list = ocr_module.test_trained_ocr(gray_img)

		for txt in detect_list:
			txt_module.print_detect_word(txt.content)

	elif args[2] == "-c":
		detected_area = img_module.ticket_threshold(args[1])
		img_module.cut_title_area(args[1], detected_area)

	elif args[2] == "-d":
		img_filter = img_module.img_proc_filter(args[1])
		img_filter.show()
		print(img_filter.width)
		print(img_filter.height)

	elif args[2] == "-s":
		img_module.test_default_model(args[1])

	elif args[2] == "-try":
		img = Image.open(args[1])
		img.show()

		img_list = glob.glob("./get_result/" + "*")
		for i in img_list:
			os.remove(i)
		#指定した画像からタイトル領域を取得する
		detected_area = img_module.ticket_threshold(args[1])

		img_module.area_img_to_ocr(args[1], detected_area)
		#OCR処理で画像を取得しておき、画像を全て表示してみる
		img_list = glob.glob("./get_result/" + "*")

		for i in img_list:
			img = Image.open(i)
			img.show()
		exit()

	elif args[2] == "-h":
		print("-t: 訓練モデル全てでタイトル画像にOCR")
		print("-c: タイトル領域を切り出す(直下にtmp.jpg)")
		print("-d: 2値画像を表示する")
		print("-s: 元のモデルでOCRする")
		print("-w: 濁点補正のデバッグ")

	else:
		print("error debug option")
	exit()

#本処理(ブラウザ上でも同じような手順を行う)
"""
領域抽出 => デフォルトのモデル
内容抽出 => 強化したモデル
で分けて使う
"""
img = Image.open(args[1])


#指定した画像からタイトル領域を取得する
#各領域の画像を./areaに書き出す(以降はこれを使って識別する)
detected_area = img_module.ticket_threshold(args[1])

print(detected_area)
