#!/usr/bin/python3 -u
# -*- encoding: utf-8 -*-
'''
@File          :   pdf_merge.py
@Time          :   2023/10/09 09:04:10
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
from PyPDF2 import PdfMerger

sys.path.append('.')
ut.starttime = time.time()

# Version history
ver = ut.ver = 'V0.1'
ver_date = ut.ver_date = 'Oct. 9, 2023'
ver_des = ut.ver_des = 'release version.'
ver_detail_des = ut.ver_detail_des = ''' creete scritps '''
scr_des = ut.scr_des = 'merge PDF file into one file'
scr_des_detail = '''
Description: merge PDF file into one file
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

    parser.add_argument('-f', '--infile', type=str, required=True, help='input\
                        PDF file(s) with ORDER for merge.')
    parser.add_argument('-o', '--outfile', type=str, required=False, default="\
                        merged.pdf", help='folder save PDF file(s)')
    parser.add_argument('-sta', '--status', type=str, choices=['RUN', 'DEBUG'],
                        help=argparse.SUPPRESS)
    return parser.parse_args()


def main_run():
    # merger = PdfFileMerger()
    merger = PdfMerger()
    for f in args.infile.split():
        merger.append(f)
    merger.write(str(args.outfile))
    ut.print_info(f"All PDF files merged into file: {args.outfile}")


# ------------------------------------------------------------
# Running  main
# ------------------------------------------------------------
if __name__ == '__main__':
    # run status:  'DEBUG' || 'INFO' || 'WARNING' || 'ERROR' || 'CRITICAL' ||
    # 'RUN':
    ut.RUN_STATUS = 'RUN'

    # additional meg in header for current scripts
    ut.header(add_msg='')

    args = parseargu()

    main_run()
    ut.footer()
