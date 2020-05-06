import utils.wordsinUnspec
from utils.load_excel import COMM_NARROW
import xlsxwriter
from xlrd import open_workbook
import operator
import utils.DeepCompare as DC
import pandas as pd

book = open_workbook('../sample_text/NormalizedEcomm.xlsx')
county_list = []
sheet = book.sheet_by_index(1)
# read header values into the list
keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(1, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    county_list.append(d)


def GensheetsCountytoUNSPSC():
    sheetNames = COMM_NARROW.get_all_sheet_names()
    for sheet in sheetNames:
        workbook = xlsxwriter.Workbook('../ignore/'+sheet+'.xlsx')
        narrowed_down_UNSPSC = pd.read_excel("../sample_text/narrowedSheets.xlsx",sheet_name=sheet).iloc[:,0]
        narrowed_commodity = pd.read_excel("../sample_text/narrowedSheets.xlsx",sheet_name=sheet).iloc[:,1]
        for i in county_list:
            if(str(int(i.get("COMM_CLS")))== sheet):
                results = DC.comparisons2(i.get("KEYWD").lower(),narrowed_down_UNSPSC)
                excelSheet = workbook.add_worksheet(str(i.get("COMM_ITM")))
                excelSheet.write(0,0,i.get("COMM_CD"))
                excelSheet.write(0,1,i.get("KEYWD"))
                excelSheet.write(1,0,"Commodity Title")
                excelSheet.write(1,1,"Commodity")
                excelSheet.write(1,2,"Similar Percent")
                countRow = 2
                countList = 0
                for entry in results:
                    excelSheet.write(countRow,0,entry[0])
                    excelSheet.write(countRow,1,narrowed_commodity[countList])
                    excelSheet.write(countRow,2,entry[1])
                    countRow += 1
                    countList += 1
        workbook.close()
                    
                
                
                
        
GensheetsCountytoUNSPSC()
    
    
