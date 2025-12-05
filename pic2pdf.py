#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#--------------------------------------------------
# Copyright (C) 2022 WayOn. All rights reserved.
# Filename      : jpg2pdf.py
# Description   :  
# Date          : 2025-12-05
# Author        : Li Guoqiang
# Email         : lgq@way-on.com
# Version       : v0.1
# History       : initial version
#--------------------------------------------------


from PIL import Image
import sys
# print(sys.argv)
print(f"usage: {sys.argv[0]} 1.jpg 2.jpg")
pdf_f = "output.pdf"
# image_paths = ['1.jpg', '2.jpg']
image_paths = sys.argv[1:]
output_pdf = pdf_f
images = [Image.open(img).convert('RGB') for img in image_paths]
images[0].save(output_pdf, save_all=True, append_images=images[1:])
print(f"output PDF: {pdf_f}")
