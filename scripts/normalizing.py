import nltk
import xlrd
import xlsxwriter
import os.path
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def workbookStuff():

	print("Checking if file exists...")

	if os.path.isfile('NormalizedUNSPSC.xlsx'):
		print("File already exists.")

	else:
		print("File does not exist.")
		print("Creating workbook...")
		workbook = xlsxwriter.Workbook('NormalizedUNSPSC.xlsx')
		worksheet = workbook.add_worksheet()
		print("Workbook created under NormalizedUNSPSC.xlsx")

		print("Opening UNSPSC...")
		loc = "C:/Users/Jordi/Desktop/Senior Design/UNSPSC English v220601 project/UNSPSC English v220601 project.xlsx"
		wb = xlrd.open_workbook(loc)
		sheet = wb.sheet_by_index(0)
		print("Opened.")

		bold = workbook.add_format({'bold': True})

		print("Writing to workbook...")
		
		rows = sheet.nrows
		cols = sheet.ncols

		for i in range(cols):
			worksheet.write(0, i, sheet.cell_value(0, i))

		for row in range(1, rows):
			for col in range(cols):
				worksheet.write(row, col, remove(sheet.cell_value(row, col)))


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


workbookStuff()