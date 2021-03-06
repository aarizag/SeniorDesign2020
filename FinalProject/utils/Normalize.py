import nltk
import xlrd
import xlsxwriter
import os.path
import progressbar
import time
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim.models as gm


print("Opening model...")
model = gm.KeyedVectors.load_word2vec_format("../models/GoogleNews-vectors-negative300.bin.gz", binary = True)
print("Model opened.")




def normalizeECOMM():
	print("Checking if NormalizedEcomm.xlsx exists...")

	if os.path.isfile('../sample_text/NormalizedEcomm.xlsx'):
		print("File already exists.")

	else:
		print("File does not exist.")
		print("Creating workbook...")
		workbook = xlsxwriter.Workbook('../sample_text/NormalizedEcomm.xlsx')
		worksheet = workbook.add_worksheet('COMM_CLS')
		worksheet2 = workbook.add_worksheet('COMM_ITM')
		print("Workbook created under NormalizedEcomm.xlsx")

		print("Opening Ecomm...")
		loc = "../sample_text/eCAPS_COMM_11072019.xlsx"
		wb = xlrd.open_workbook(loc)
		sheet = wb.sheet_by_index(1)
		sheet2 = wb.sheet_by_index(2)
		print("Opened.")

		rows = sheet.nrows
		cols = sheet.ncols
		rows2 = sheet2.nrows
		cols2 = sheet2.ncols
		for col in range(cols):
			worksheet.write(0, col, sheet.cell_value(0, col))
		for col in range(cols2):
			worksheet2.write(0, col, sheet.cell_value(0, col))
			

		bar = progressbar.ProgressBar(maxval=rows+rows2, \
	    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start()
		for row in range(1,rows):
			for col in range(cols):
				bar.update(row+1)
				if type(sheet.cell_value(row, col)) == float:
					worksheet.write(row, col, remove(str(sheet.cell_value(row, col))))
				else:
					worksheet.write(row, col, remove(str(sheet.cell_value(row, col))).lower())

		for row in range(1,rows2):
			for col in range(cols2):
				bar.update(row+1)
				if type(sheet2.cell_value(row, col)) == float:
					worksheet2.write(row, col, remove(str(sheet2.cell_value(row, col))))
				else:
					worksheet2.write(row, col, remove(str(sheet2.cell_value(row, col))).lower())
		bar.finish()
		workbook.close()

def normalizeUNSPSC():

	print("Checking if NormalizedUNSPSC.xlsx exists...")

	if os.path.isfile('../sample_text/NormalizedUNSPSC.xlsx'):
		print("File already exists.")

	else:
		print("File does not exist.")
		print("Creating workbook...")
		workbook = xlsxwriter.Workbook('../sample_text/NormalizedUNSPSC.xlsx')
		worksheet = workbook.add_worksheet()
		print("Workbook created under NormalizedUNSPSC.xlsx")

		print("Opening UNSPSC...")
		loc = "../sample_text/UNSPSC English v220601 project.xlsx"
		wb = xlrd.open_workbook(loc)
		sheet = wb.sheet_by_index(0)
		print("Opened.")


		print("Writing to workbook...")
		
		rows = sheet.nrows
		cols = sheet.ncols
		bold = workbook.add_format({'bold': True})


		for i in range(1,cols):
			worksheet.write(0, i-1, sheet.cell_value(0, i), bold)

		bar = progressbar.ProgressBar(maxval=rows, \
	    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start()

		for row in range(1, rows):
			for col in range(1, cols - 2):
				if row < 5:
					continue
				else:
					bar.update(row+1)
					if type(sheet.cell_value(row, col)) == float:
						worksheet.write(row, col-1, remove(str(int(sheet.cell_value(row, col)))))
					else:
						worksheet.write(row, col-1, remove(str(sheet.cell_value(row, col))).lower())
		bar.finish()
		workbook.close()



def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def remove(sent):

	if(sent.isnumeric()):
		return sent
	else:
		phrase = sent

		phrase = phrase.lower()
		#removing punc
		tokenizer = RegexpTokenizer(r'\w+')
		phraseList = tokenizer.tokenize(phrase)
		stop_words = set(stopwords.words('english'))
		filtered_sentence = []

		for w in phraseList:
			if w not in stop_words:
				if hasNumbers(w):
					continue
				else:
					try:
						model.word_vec(w.lower())
					except KeyError:
						continue
					else:
						filtered_sentence.append(w)
		newSent = ' '.join([str(elem) for elem in filtered_sentence])


		return newSent



normalizeUNSPSC()
normalizeECOMM()

