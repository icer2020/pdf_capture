#!/usr/bin/python3 -u
# -*- encoding: utf-8 -*-
# -- coding: utf-8 --
# 导入PYPDF2库
from PyPDF2 import PdfReader, PdfWriter

# use module
from modules import utils_wo as ut
from modules import local_class as lc

import os
import re
import sys
import time

import argparse
import datetime

# Version history
tool = sys.argv[0].split('/')[-1]
ver = 'V0.10'
ver_build_date = 'Jun. 14, 2024'
ver_des = 'initial verseion'
ver_detail_des = ''' 
inital version
'''
ver_info = f'{tool+" version":<30s}{ver:>15s}\n{tool+" build date":<30s}{ver_build_date:>15s}'

scr_des = "PDF split tool"
scr_des_detail = '''
Description: split PDF with specified page per-file between start and end page"
Feedback/bug email to: lgq@way-on.com 
'''

starttime = time.time()

ut.ver = ver
ut.ver_build_date = ver_build_date
ut.ver_des = ver_des
ut.ver_detail_des = ver_detail_des
ut.scr_des = scr_des
ut.starttime = starttime


# ------------------------------------------------------------
# function section
# ------------------------------------------------------------
def parseargu():
    global ver
    global ver_date
    global ver_des
    post_msg = ver.ljust(20) + ver_des.center(40) + ver_build_date.rjust(20)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=scr_des_detail, epilog=post_msg)



    parser.add_argument('-i', '--input', required=True,
                        help='Input file for PDF split')
    parser.add_argument('-o', '--output_folder', required=False,
                        help='Output folder for splied PDF(s)',
                        default='pdf_split')
    parser.add_argument('-s', '--start', required=False,
                        help='PDF page start. Default page 1')
    parser.add_argument('-e', '--end', required=False,
                        help='PDF page end. Default page END')
    parser.add_argument('-g', '--grid', required=False,
                        help='page count split per-PDF from page start to page end',
                        default='1')

    parser.add_argument('-sta', '--status', type=str, choices=['RUN', 'DEBUG'],
                        help=argparse.SUPPRESS)

    args_l = parser.parse_args()
    return args_l


def main_run():
    create_folder(args.output_folder)
    # 1. 获取原始pdf文件
    fp_read_file = open(args.input, 'rb')
    # fp_read_file.close()
    # 2. 将要分割的PDF内容格式化
    pdf_input = PdfReader(fp_read_file)
    # 3. 实例一个 PDF文件编写器
    pdf_output = PdfWriter()

    pages = len(pdf_input.pages)
    ut.print_info(f'PDF {args.input} total pages: {pages}')

    if args.start:
        s = int(args.start)
    else:
        s = 1
    if args.end:
        e = int(args.end)
    else:
        e = pages


    grid = int(args.grid)

    cnt = 0
    for i in range(s-1, e, grid):
        if i +grid > pages:
            grid = pages - i
        cnt += 1
        fo = args.output_folder + os.sep + re.sub('\.pdf', "", args.input) + "_part" + str(cnt).zfill(2) + "_" + str(i+1) + "_" + str(i+grid) + ".pdf"
        pdf_output = PdfWriter()
        for j in range(i, i+grid):
            # j = pages -1 if  j > pages-1 else j
            pdf_output.add_page(pdf_input.pages[j])
        with open(fo, 'wb') as pdf_out:
            pdf_output.write(pdf_out)
        ut.print_info(f'PDF pages {str(i+1)} to {str(i+grid)} saveas into file: {fo} (pages: {grid})')

    
    ut.print_info(f'Total PDF {cnt} split file(s) saved)')

    # 4. 把3到4页放到PDF文件编写器
    # for i in range(s-1, e):
    #     print(i)
    #     pdf_output.add_page(pdf_input.pages[i])
    # # 5. PDF文件输出
    fp_read_file.close()
    return 0


def create_folder(path, cleanup=True):
    if cleanup:
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    try:
        os.mkdir(path)
    except:
        None
    return path


# if __name__ == '__main__':
#     # 待切分文件文件名
#     in_pdf_name = "2020暑假二年级创新数学加油站.pdf"
#     # 切分后文件文件名
#     out_pdf_name = 'split.pdf'
#     # 切分开始页面
#     start = 3
#     # 切分结束页面
#     end = 4
#     split_single_pdf(in_pdf_name, start, end, out_pdf_name)

if __name__ == "__main__":
    ut.RUN_STATUS = 'RUN'
    # additional meg in header for current scripts
    ut.header(add_msg='')

    args = parseargu()
    main_run()

    ut.footer()


