# import pdfplumber
# with pdfplumber.open(r'1.pdf') as pdf:
#     first_page = pdf.pages[0]
#     # print(first_page.extract_text())
#     print(first_page.extract_tables())


'''
import os
import fitz
import shutil
#     支持滴滴行程单。
#     # PyMuPDF模块：https://pymupdf.readthedocs.io/en/latest/tutorial.html#extracting-text-and-images
root_dir = "./"
out_dir = "./output"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
 
 
def fapiao_read(text):
    if "￥" in text:
        print(text.split("￥")[-1].split("\n")[0])
        money = text.split("￥")[-1].split("\n")[0]
    elif "¥" in text:
        print(text.split("¥")[-1].split("\n")[0])
        money = text.split("¥")[-1].split("\n")[0]
    return money
 
 
def xingchengdan_read(text):
    print(text.split("合计")[1].split("元")[0].split()[0])
    money = text.split("合计")[1].split("元")[0].split()[0]
    return money
 
 
Repeat_name_list = []
for file in os.listdir("./"):
    if file.endswith(".pdf"):
        src = os.path.join(root_dir, file)
        doc = fitz.open(src)  # or fitz.Document(filename)
        page = doc.load_page(0)
        text = page.get_text("text")
        print(text)
 
        if "￥" in text or "¥" in text:
            if "敏感信息脱敏" in text and "敏感信息脱敏" in text:
                money = fapiao_read(text)
                out_file_name = "电子发票" + money + "元"
            else:
                continue
        else:
            money = xingchengdan_read(text)
            out_file_name = "电子发票" + money + "元行程单"
        Repeat_name_list.append(out_file_name)
        if out_file_name in Repeat_name_list:
            repeat_num = Repeat_name_list.count(out_file_name)
            if repeat_num == 1:
                out_file_name = out_file_name
            else:
                out_file_name = out_file_name + "(" + str(repeat_num-1) + ")"
        dst = os.path.join(out_dir, out_file_name+".pdf")
        shutil.copy(src, dst)
'''

import camelot.io as camelot
# import Camelot.io as Camelot
receipt = "1.pdf"
tables = camelot.read_pdf(receipt, shift_text=[''], strip_text='\n')
table = tables[0].df  # 将发票表格转换为dataframe
price = table[10][2][1:]
if len(price) == 0:
    price = table[9][2][-6:]

print(price)
