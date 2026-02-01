#!python.exe -u
# -*- coding: utf-8 -*-
#--------------------------------------------------
# Copyright (C) 2022 WayOn. All rights reserved.
# Filename      : pdf_pagg_cut_by_half.py
# Description   :  
# Date          : 2025-12-29
# Author        : Li Guoqiang
# Email         : lgq@way-on.com
# Version       : v0.1
# History       : initial version
#--------------------------------------------------

from PyPDF2 import PdfReader, PdfWriter
import sys
from pathlib import Path

def split_pdf(infile, outfile):
    all_page = PdfWriter()

    with open(infile, 'rb') as infile:
        pdfReader = PdfReader(infile)
        number_of_pages = len(pdfReader.pages)
        for i in range(number_of_pages):
            page = pdfReader.pages[i]
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            if width >= height:
                r_w = width
                r_h = height
            else:
                r_h = width
                r_w = height
            print(f'page: {i} , width/height: {width}/{height}')

            pdfReader = PdfReader(infile)
            pdfWriter = PdfWriter()
            page_top = pdfReader.pages[i]

            ll = (0, 0)
            lr = (width/2, 0)
            ul = (0, height)                  
            ur = (width/2, height)

            page_top.mediabox.lower_left  = ll
            page_top.mediabox.lower_right = lr
            page_top.mediabox.upper_left  = ul
            page_top.mediabox.upper_right = ur


            pdfWriter.add_page(page_top)

            # botton page
            pdfReader = PdfReader(infile)
            pdfwriter = PdfWriter()
            page_bottom = pdfReader.pages[i]

            page_bottom.mediabox.lower_left = (width/2, 0)
            page_bottom.mediabox.lower_right = (width, 0)
            page_bottom.mediabox.upper_left = (width/2, height)
            page_bottom.mediabox.upper_right = (width, height)

            pdfwriter.add_page(page_bottom)

            all_page.add_page(page_top)
            all_page.add_page(page_bottom)

    with open(outfile, 'wb') as fo:
        all_page.write(fo)
    print(f'-I- check page cut in file: {outfile}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} input.pdf output.pdf")
    else:
        split_pdf(sys.argv[1], sys.argv[2])
