import camelot.io as camelot
import os
# import pprint
# import shutil

fo_file = 'summary.txt'
fo_sum = open(fo_file, 'w', encoding="utf-8")
def seek_files(id1, name):
    file_name = []
    for root, dirs, files in os.walk(id1):
        for fn in files:
            if ".pdf" in fn:
                fn_full = root + "/" + fn
                file_name.append(fn_full)
    return file_name


# file_name = seek_files("pdf", "pdf")
file_name = seek_files("20220610", "pdf")

sum = 0
file_price = dict()
for receipt in file_name:
    price = "NA"
    # shutil.copy(f, receipt)
    print("-I-: parse file:", receipt)
    tables = camelot.read_pdf(receipt, shift_text=[''], strip_text='\n')
    table = tables[0].df  # 将发票表格转换为dataframe
    # price = table[10][2][1:]
    if len(table.columns) == 6:
        clm = len(table.columns) - 1 
    else:
        clm = len(table.columns) - 2 
    price = table[clm][2][1:]
    # print("==", table[clm][2].split())
    # print('1-price', price)
    try:
        price = float(price)
    except:
        price = table[clm][2][5:]

    try:
        price = float(price)
    except:
        print("-E- file {:} price is not float/int please check".format(receipt))

    # if len(price) == 0:
    #     price = table[9][2][-6:]
    #     print('2-price', price)
    sum += float(price)
    file_price[receipt] = price


outline = "{:<60}{:>20}".format("file", "price")
# print(outline)
fo_sum.writelines(outline+"\n")

outline = "-"*140
# print(outline)
fo_sum.writelines(outline+"\n")

for n in sorted(file_price.keys()):
    outline = "{:<60}{:>20}".format(n, file_price[n])
    # print(outline)
    fo_sum.writelines(outline+"\n")

outline = "="*140
# print(outline)
fo_sum.writelines(outline+"\n")

outline = ("{:<60}{:>20}".format(len(file_price.keys()), sum))
# print(outline)
fo_sum.writelines(outline+"\n")

fo_sum.close()

print("-I-: total {:} file(s) are parse. Total fee are {:}. Detail is in file: {:}".format(len(file_price.keys()), sum, fo_file))
