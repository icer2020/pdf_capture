#!python.exe -u
# -*- coding: utf-8 -*-
#--------------------------------------------------
# Copyright (C) 2022 WayOn. All rights reserved.
# Filename      : pdf_rotate.py
# Description   :  
# Date          : 2025-12-29
# Author        : Li Guoqiang
# Email         : lgq@way-on.com
# Version       : v0.1
# History       : initial version
#--------------------------------------------------

from pypdf import PdfReader, PdfWriter
import re, sys

def rotate_pdf(input_file, output_file, rotation):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(rotation)
        page.transfer_rotation_to_content()
        writer.add_page(page)
    with open(output_file, "wb") as f:
        writer.write(f)
    print(f'-I- check rotated PDF in file: {output_file}')

if len(sys.argv) != 4:
    print(f"usage: {sys.argv[0]} input.pdf clock_with_degree(90/180/270) output.pdf")
else:
    rotate_pdf(sys.argv[1], sys.argv[3], int(sys.argv[2]))
