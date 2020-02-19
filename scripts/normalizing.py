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

		#writing titles
		for i in range(cols - 2):
			worksheet.write(0,i ,sheet.cell_value(12,i), bold)

		#keys
		for j in range(rows):
			if sheet.cell_value(j,1) == 'Key':
				continue
			else:
				worksheet.write(j,1, sheet.cell_value(j,1))

		for i in range(rows):
			if sheet.cell_value(i,2) == 'Segment':
				continue
			else:
				worksheet.write(i,2, sheet.cell_value(i,2))

		
		for i in range(rows):
			if sheet.cell_value(i,3) == 'Segment Title':
				continue
			else:
				if i < 5:
					continue
				else:
					worksheet.write(i,3, remove(sheet.cell_value(i,3)))

		for i in range(rows):
			if sheet.cell_value(i,4) == 'Segment Definition':
				continue
			else:
				worksheet.write(i,4, remove(sheet.cell_value(i,4)))

		for i in range(rows):
			if sheet.cell_value(i,5) == 'Family':
				continue
			else:
				worksheet.write(i,5, sheet.cell_value(i,5))

		for i in range(rows):
			if sheet.cell_value(i,6) == 'Family Title':
				continue
			else:
				worksheet.write(i,6, remove(sheet.cell_value(i,6)))

		for i in range(rows):
			if sheet.cell_value(i,7) == 'Family Definition':
				continue
			else:
				worksheet.write(i,7, remove(sheet.cell_value(i,7)))

		for i in range(rows):
			if sheet.cell_value(i,8) == 'Class':
				continue
			else:
				worksheet.write(i,8, sheet.cell_value(i,8))

		for i in range(rows):
			if sheet.cell_value(i,9) == 'Class Title':
				continue
			else:
				worksheet.write(i,9, remove(sheet.cell_value(i,9)))

		for i in range(rows):
			if sheet.cell_value(i,10) == 'Class Definition':
				continue
			else:
				worksheet.write(i,10, remove(sheet.cell_value(i,10)))

		for i in range(rows):
			if sheet.cell_value(i,11) == 'Commodity':
				continue
			else:
				worksheet.write(i,11, sheet.cell_value(i,11))
		for i in range(rows):
			if sheet.cell_value(i,12) == 'Commodity Title':
				continue
			else:
				worksheet.write(i,12, remove(sheet.cell_value(i,12)))

		for i in range(rows):
			if sheet.cell_value(i,13) == 'Commodity Definition':
				continue
			else:
				worksheet.write(i,13, remove(sheet.cell_value(i,13)))
		workbook.close()
		print("Done.")



def remove(sent):
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