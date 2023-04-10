#!/usr/bin/python3 -u
# -*- encoding: utf-8 -*-
'''
@File          :   pdf_capture_receipt.py
@Time          :   2023/04/06 09:04:10
@Author        :   ICer
@Version       :   0.1
@Contact       :   i_chip_backend@163.com
@WebSite       :   https://blog.csdn.net/i_chip_backend
@License       :   (C)Copyright 2018-2023, ICerDev
@Description   :   initial version
'''
import argparse
import time
import utils as ut
import sys
import camelot.io as camelot
import os

sys.path.append('.')
ut.starttime = time.time()

# Version history
ver = ut.ver = 'V0.1'
ver_date = ut.ver_date = 'Apr. 6, 2023'
ver_des = ut.ver_des = 'release version.'
ver_detail_des = ut.ver_detail_des = ''' creete scritps '''
scr_des = ut.scr_des = 'pick-up the fee from e-receipt'
scr_des_detail = '''
Description: recognize the total fee from Chinese tax e-receipt
'''

# ------------------------------------------------------------
# function section
# ------------------------------------------------------------
def parseargu():
    global ver
    global ver_date
    global ver_des
    post_msg = ver.ljust(18) + ver_des.center(40) + ver_date.rjust(18)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=scr_des_detail, epilog=post_msg)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', type=str, help='input PDF file(s)')
    group.add_argument('-p', '--path', type=str, help='folder save PDF file(s)')
    parser.add_argument('-sta', '--status', type=str, choices=['RUN', 'DEBUG'],
                        help=argparse.SUPPRESS)
    return parser.parse_args()


def seek_files(id1, name):
    file_name = []
    for root, dirs, files in os.walk(id1):
        for fn in files:
            if ".pdf" in fn:
                fn_full = root + "/" + fn
                file_name.append(fn_full)
    return file_name
 
def main_run():
    fo_file = 'summary.txt'
    fo_sum = open(fo_file, 'w', encoding="utf-8")
   
    if args.path:
        file_name = seek_files(args.path, "pdf")
    else:
        file_name = args.file.split()

    
    sum = 0
    file_price = dict()
    for receipt in file_name:
        price = "NA"
        ut.print_info("Parse file:", receipt)
        tables = camelot.read_pdf(receipt, shift_text=[''], strip_text='\n')
        table = tables[0].df 
        if len(table.columns) == 6:
            clm = len(table.columns) - 1 
        else:
            clm = len(table.columns) - 2 
        price = table[clm][2][1:]
        try:
            price = float(price)
        except:
            price = table[clm][2][5:]
    
        try:
            price = float(price)
        except:
            ut.print_error("File {:} price is not float/int please check".format(receipt))
    
        sum += float(price)
        file_price[receipt] = price
    
    outline = "{:<60}{:>20}".format("file", "price")
    fo_sum.writelines(outline+"\n")
    
    outline = "-"*140
    fo_sum.writelines(outline+"\n")
    
    for n in sorted(file_price.keys()):
        outline = "{:<60}{:>20}".format(n, file_price[n])
        fo_sum.writelines(outline+"\n")
    
    outline = "="*140
    fo_sum.writelines(outline+"\n")
    
    outline = ("{:<60}{:>20}".format(len(file_price.keys()), sum))
    fo_sum.writelines(outline+"\n")
    
    fo_sum.close()
    
    ut.print_info("总计发票数量：{:} 费用总计：{:} Detail is in file: {:}".format(len(file_price.keys()), sum, fo_file))


# ------------------------------------------------------------
# Running  main
# ------------------------------------------------------------
if __name__ == '__main__':
    # run status:  'DEBUG' || 'INFO' || 'WARNING' || 'ERROR' || 'CRITICAL' || 'RUN':
    ut.RUN_STATUS = 'RUN'

    # additional meg in header for current scripts
    ut.header(add_msg='')

    args = parseargu()

    main_run()
    ut.footer()



