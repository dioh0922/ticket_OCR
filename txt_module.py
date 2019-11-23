import jaconv

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
