from spire.pdf import PdfDocument
from spire.pdf import PdfTextExtractOptions
from spire.pdf import PdfTextExtractor

import subprocess

cmd = 'ls *pdf'
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# for i in p.stdout.readline().decode("gbk",  "ignore"):
for i in p.stdout.readlines():
    pdf_f_p=str(i.decode("gbk",  "ignore").strip())
    txt_f_p=pdf_f_p.replace('.pdf','.txt')

    pdf_f=str(i.decode("utf-8",  "ignore").strip())
    txt_f=pdf_f.replace('.pdf','.txt')
    print(f'{pdf_f_p} -> {txt_f_p}')

    pdf = PdfDocument()
    # pdf.LoadFromFile("肝功十项_血脂四项_肾功四项.pdf")
    pdf.LoadFromFile(pdf_f)
    
    # 创建一个字符串对象来存储文本
    extracted_text = ""
    
    # 创建PdfExtractor对象
    extract_options = PdfTextExtractOptions()
    
    # 循环遍历文档中的页面
    for i in range(pdf.Pages.Count):
        # 获取页面
        page = pdf.Pages.get_Item(i)
        # 创建PdfTextExtractor对象，并将页面作为参数传递
        text_extractor = PdfTextExtractor(page)
        # 从页面中提取文本
        text = text_extractor.ExtractText(extract_options)
        # 将提取的文本添加到字符串对象中
        extracted_text += text
    
    # 将提取的文本写入文本文件
    # with open("1.txt", "w") as file:
    with open(txt_f, "w") as file:
        file.write(extracted_text)
    pdf.Close()

