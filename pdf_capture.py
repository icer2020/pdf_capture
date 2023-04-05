#!/usr/bin/python3 -u
# -*- encoding: utf-8 -*-
'''
@File          :   pdf_capture.py
@Time          :   2023/04/05 21:14:28
@Author        :   ICer
@Version       :   0.1
@Contact       :   i_chip_backend@163.com
@WebSite       :   https://blog.csdn.net/i_chip_backend
@License       :   (C)Copyright 2018-2023, ICerDev
@Description   :   1st release version
'''
import PIL.Image as Image
import argparse
import cv2
import fitz
import os
import random
import shutil
import sys
import time
import utils as ut

ut.starttime = time.time()

# Version history
ver = ut.ver = 'V0.1'
ver_date = ut.ver_date = 'Apr. 05, 2023'
ver_des = ut.ver_des = '1st release version.'
ver_detail_des = ut.ver_detail_des = ''' scritps release '''
scr_des = ut.scr_des = 'PDF capture for combined word-card'
scr_des_detail = '''
Description: Translate HongEn basic-word PDF into word-only combined PDF for kid use
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

    parser.add_argument('-i', '--in_file', required=False,
                        help='Input file',
                        default='./1-200.pdf')
    parser.add_argument('-o', '--out_file', required=False,
                        help='Output file',
                        default='./combined.pdf')
    parser.add_argument('-sta', '--status', type=str, choices=['RUN', 'DEBUG'],
                        help=argparse.SUPPRESS)
    parser.add_argument('-k', '--keep_temp_file', action='store_false',
                        help='keep temp png/final pic file')

    args_l = parser.parse_args()
    return args_l


def pyMuPDF2_fitz(pdfPath, imagePath):
    # open pdf
    pdfDoc = fitz.open(pdfPath) 
    # iterate through the pages
    ut.print_info("Analysis pdf file: ", args.in_file)
    for pg in range(pdfDoc.page_count): 
        if pg % 10 ==0:
            ut.print_info("Check page: ", pg)
        page = pdfDoc[pg]
        rotate = int(0)
        # PDF zoom ratio
        zoom_x = 3
        zoom_y = 3

        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        rect = page.rect

        grid = 145
        x1 = 10
        x2 = x1 + 91
        y1 = 88 + grid
        y2 = y1 + (180-88)
        clip = fitz.Rect(x1, y1, x2, y2)

        j = 0
        for i in range(5):
            grid = 145
            x1 = 10
            x2 = x1 + 91
            y1 = 88 + grid*i
            y2 = y1 + (180-88)
            clip = fitz.Rect(x1, y1, x2, y2)
            pix = page.get_pixmap(matrix=mat, alpha=False, clip=clip)
            if not os.path.exists(imagePath):
                os.makedirs(imagePath)
            pix.save(f'{imagePath}/{str(pg).zfill(3)}_{str(i).zfill(3)}.png')

def image_compose():
    IMAGES_PATH = imagePath
    IMAGES_FORMAT = ['.png']

    IMAGE_SIZE_X = 273 
    IMAGE_SIZE_Y = 273 
    IMAGE_ROW = 9 
    IMAGE_COLUMN = 6
    space_x = 6
    space_y = 6
    margin_x = 120
    margin_y = 70

    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if os.path.splitext(name)[1] == item]

    image_width = 1900
    image_height = int(image_width * pow(2, 0.5))
    random.shuffle(image_names)
    img_total_cnt = len(image_names)
    if img_total_cnt % (IMAGE_COLUMN*IMAGE_ROW) == 0:
        total_page = int(img_total_cnt/float(IMAGE_COLUMN*IMAGE_ROW))
    else:
        total_page = int(img_total_cnt/float(IMAGE_COLUMN*IMAGE_ROW)) + 1
        
    img_cnt = 0
    index_cnt = 1
    img_file_name = []
    while img_cnt<img_total_cnt:
        for y in range(IMAGE_ROW):
            for x in range(IMAGE_COLUMN):
                if img_cnt ==0:
                    to_image = Image.new('RGB', (image_width, image_height), "white")
                    IMAGE_SAVE_PATH = 'final_' + str(index_cnt) + '.jpg'
                elif img_cnt % (IMAGE_ROW*IMAGE_COLUMN)==0:
                    to_image.save(IMAGE_SAVE_PATH)
                    p_page = "-" + str(index_cnt)+"/"+str(total_page) + "-"
                    add_page(IMAGE_SAVE_PATH, p_page)
                    img_file_name.append(IMAGE_SAVE_PATH)
                    ut.print_debug("IMAGE_SAVE_PATH: {:} img_cnt: {:}".format(IMAGE_SAVE_PATH, img_cnt))
                    index_cnt += 1
                    to_image = Image.new('RGB', (image_width, image_height), "white")
                    IMAGE_SAVE_PATH = 'final_' + str(index_cnt) + '.jpg'
                point_x = margin_x + x*IMAGE_SIZE_X + x*space_x 
                point_y = margin_y + y*IMAGE_SIZE_Y + y*space_y
                if img_cnt < img_total_cnt:
                    img_f = IMAGES_PATH + "/" + image_names[img_cnt] 
                    to_image.paste(Image.open(img_f), (point_x, point_y))
                    img_cnt += 1
                else:
                    to_image.save(IMAGE_SAVE_PATH)
                    p_page = "-" + str(int(index_cnt))+"/"+str(total_page) + "-"
                    add_page(IMAGE_SAVE_PATH, p_page)
                    img_file_name.append(IMAGE_SAVE_PATH)
                    ut.print_debug("final save IMAGE_SAVE_PATH: {:} img_cnt: {:}".format(IMAGE_SAVE_PATH, img_cnt))
                    break
            if img_cnt >= img_total_cnt:
                break
    doc = fitz.open()
    for img_file in img_file_name:
        imgdoc = fitz.open(img_file)
        pdfbytes = imgdoc.convert_to_pdf()
        pdf_name = str(img_file) + '.pdf'
        imgpdf = fitz.open(pdf_name, pdfbytes)
        doc.insert_pdf(imgpdf)
    doc.save(args.out_file)
    doc.close()

    if args.keep_temp_file:
        for img_file in img_file_name:
            os.remove(img_file)
    
def add_page(img_file, number):
    bk_img = cv2.imread(img_file)
    size = bk_img.shape
    w = size[1] 
    h = size[0]
    cv2.putText(bk_img, str(number), (int(size[1]/2-80),int(size[0]-30)), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,0), 3, cv2.LINE_AA)
    cv2.imwrite(img_file, bk_img)


# ------------------------------------------------------------
# Running  main
# ------------------------------------------------------------
if __name__ == "__main__":
    ut.RUN_STATUS = 'RUN'
    # additional meg in header for current scripts
    ut.header(add_msg='')

    args = parseargu()

    imagePath = 'png'
    if not args.keep_temp_file:
        ut.print_info("Run with keep temp png/final file")

    ut.print_debug("Remove existing path:", imagePath)
    if os.path.isdir(imagePath):
        shutil.rmtree(imagePath)

    ut.print_debug('Remove existing file: final_*.jpg', )
    for root, dirs, files in os.walk('.'):
        for fn in files:
            if "final_" in fn and ".jpg" in fn:
                os.remove(fn)
    pyMuPDF2_fitz(args.in_file, imagePath)
    image_compose()

    # rm png folder
    if args.keep_temp_file:
        shutil.rmtree(imagePath)

    ut.print_info("Check resunts in file: ",args.out_file)
    ut.footer()


