import nltk
import xlrd
import xlsxwriter
import os.path
import progressbar
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def remove(sent):
	if type(sent) == float or type(set) == int:
		return sent

	word = ""
	phrase = sent

	phrase = phrase.lower()
	#removing punc
	tokenizer = RegexpTokenizer(r'\w+')
	phraseList = tokenizer.tokenize(phrase)
	phrase = ""
	for i in range(len(phraseList)):
		phrase = phrase + phraseList[i] + " "

	stop_words = set(stopwords.words('english'))
	word_tokens = word_tokenize(phrase)
	filtered_sentence = [w for w in word_tokens if not w in stop_words]
	filtered_sentence = []

	for w in word_tokens:
		if w not in stop_words:
			filtered_sentence.append(w)

	newSent = ' '.join([str(elem) for elem in filtered_sentence])
	return newSent

print("Checking if file exists...")

if os.path.isfile('NormalizedEcomm.xlsx'):
	print("File already exists.")

else:
	print("File does not exist.")
	print("Creating workbook...")
	workbook = xlsxwriter.Workbook('NormalizedEcomm.xlsx')
	worksheet = workbook.add_worksheet('COMM_CLS')
	worksheet2 = workbook.add_worksheet('COMM_ITM')
	print("Workbook created under NormalizedEcomm.xlsx")

	print("Opening Ecomm...")
	loc = "../ignore/eCAPS_COMM_11072019.xlsx"
	wb = xlrd.open_workbook(loc)
	sheet = wb.sheet_by_index(1)
	sheet2 = wb.sheet_by_index(2)
	print("Opened.")

	rows = sheet.nrows
	cols = sheet.ncols
	rows2 = sheet2.nrows
	cols2 = sheet2.ncols


	bar = progressbar.ProgressBar(maxval=rows+rows2, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	for row in range(rows):
		for col in range(cols):
			bar.update(row+1)
			if type(sheet.cell_value(row, col)) == float:
				worksheet.write(row, col, remove(sheet.cell_value(row, col)))
			else:
				worksheet.write(row, col, remove(sheet.cell_value(row, col)).upper())

	for row in range(rows2):
		for col in range(cols2):
			bar.update(row+1)
			if type(sheet2.cell_value(row, col)) == float:
				worksheet2.write(row, col, remove(sheet2.cell_value(row, col)))
			else:
				worksheet2.write(row, col, remove(sheet2.cell_value(row, col)).upper())
	bar.finish()
	workbook.close()
