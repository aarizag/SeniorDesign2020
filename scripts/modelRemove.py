import gensim.models as gm
import os.path
import time
import xlrd
import xlsxwriter

print("Checking if file exists.")
if os.path.isfile('UNSPSCNotIn.xlsx'):
	print("File already exists.")
else:
	start = time.time()

	print("Opening UNSPSC...")
	loc = "C:/your/path/here/NormalizedUNSPSC.xlsx"
	wb = xlrd.open_workbook(loc)
	sheet = wb.sheet_by_index(0)
	print("File opened in", time.time() - start, "seconds.")

	start = time.time()

	print("Opening model...")
	model = gm.KeyedVectors.load_word2vec_format('C:/Users/Jordi/Desktop/Senior Design/GoogleNews-vectors-negative300.bin.gz', binary = True)
	print("Model opened in", time.time() - start, "seconds.")

	workbook = xlsxwriter.Workbook('UNSPSCNotIn.xlsx')
	worksheet = workbook.add_worksheet()
	print("Workbook created under UNSPSCNotIn.")

	rows = sheet.nrows
	cols = sheet.ncols
	curr = []
	thing = []




	print("Checking...")
	for row in range(1, rows):
		for col in range(cols):
			if type(sheet.cell_value(row, col)) == float:
				continue
			else:
				curr = sheet.cell_value(row, col).split()
				for word in curr:
					try:
						model.word_vec(word)
					except KeyError:
						thing.append(word)

	print("Writing to workbook...")
	thing = list(dict.fromkeys(thing))

	i = 0
	for word in thing:
		worksheet.write(i, 0, word)
		i += 1
	print("Done")
			


	# for i in range(rows):
	# 	if sheet.cell_value(i,3) == 'Segment Title' or i < 5:
	# 		continue
	# 	else:
	# 		curr = sheet.cell_value(i,3).split()
	# 		for word in curr:
	# 			try:
	# 				model.word_vec(word)
	# 			except KeyError:
	# 				worksheet.write(i, 0, word)

	workbook.close()
