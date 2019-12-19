
DICTIONARY = {
	"言己": "記",
	"カ\"" : "ガ",
	"宇)" : "字)",
	"宇）": "字)",
	"幼安": "幼女",
	"培場": "劇場",
	"剖場": "劇場",
	"-" : "ー"
}

#指定した文字列を辞書に登録してあるパターンに補正する
def revision_from_dictionary(txt):
	result = txt.replace(" ", "")
	for i in DICTIONARY:
		result = result.replace(i, DICTIONARY[i])

	return result
