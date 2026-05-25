#!/usr/bin/python3 -u
# -*- encoding: utf-8 -*-
'''
@File          :   pdf_toolbox.py
@Time          :   2026/05/25 10:04:10
@Author        :   ICer
@Version       :   1.0
@Contact       :   i_chip_backend@163.com
@WebSite       :   https://blog.csdn.net/i_chip_backend
@License       :   (C)Copyright 2018-2026, ICerDev
@Description   :   unified PDF manipulation toolbox
'''
from pypdf import PdfReader, PdfWriter, PdfMerger
from PIL import Image
import camelot.io as camelot
import cv2
import fitz
import utils as ut

import argparse
import os
import random
import re
import shutil
import sys
import time

sys.path.append('.')
ut.starttime = time.time()

ver = ut.ver = 'V1.0'
ver_date = ut.ver_date = 'May. 25, 2026'
ver_des = ut.ver_des = 'unified version.'
ver_detail_des = ut.ver_detail_des = ''' merge all PDF scripts into one class '''
scr_des = ut.scr_des = 'PDF Toolbox'
scr_des_detail = '''
Description: unified PDF manipulation toolbox with rotate/split/merge/cut/convert/capture
'''


class PDFToolbox:

    @staticmethod
    def rotate(input_file, output_file, rotation):
        reader = PdfReader(input_file)
        writer = PdfWriter()
        for page in reader.pages:
            page.rotate(rotation)
            page.transfer_rotation_to_content()
            writer.add_page(page)
        with open(output_file, "wb") as f:
            writer.write(f)
        ut.print_info(f'Rotated PDF saved: {output_file}')

    @staticmethod
    def merge(input_files, output_file):
        merger = PdfMerger()
        for f in input_files:
            merger.append(f)
        merger.write(str(output_file))
        ut.print_info(f'Merged PDF saved: {output_file}')

    @staticmethod
    def split(input_file, output_folder, start=None, end=None, grid=1):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(input_file, 'rb') as fp:
            pdf_input = PdfReader(fp)
            pages = len(pdf_input.pages)
            ut.print_info(f'PDF {input_file} total pages: {pages}')

            s = start if start else 1
            e = end if end else pages

            cnt = 0
            for i in range(s - 1, e, grid):
                g = grid
                if i + g > pages:
                    g = pages - i
                cnt += 1
                base = re.sub(r'\.pdf$', '', os.path.basename(input_file))
                fo = os.path.join(
                    output_folder,
                    f'{base}_part{str(cnt).zfill(2)}_{i + 1}_{i + g}.pdf'
                )
                pdf_output = PdfWriter()
                for j in range(i, i + g):
                    pdf_output.add_page(pdf_input.pages[j])
                with open(fo, 'wb') as pdf_out:
                    pdf_output.write(pdf_out)
                ut.print_info(f'Pages {i + 1} to {i + g} -> {fo}')

        ut.print_info(f'Total {cnt} split file(s) saved')

    @staticmethod
    def page_cut_by_half(input_file, output_file, horizontal=False):
        from pypdf.generic import RectangleObject

        def set_page_boxes(page, rect):
            page.mediabox = rect
            page.cropbox = rect
            if '/TrimBox' in page:
                page.trimbox = rect
            if '/BleedBox' in page:
                page.bleedbox = rect
            if '/ArtBox' in page:
                page.artbox = rect

        all_page = PdfWriter()
        with open(input_file, 'rb') as fp:
            reader1 = PdfReader(fp)
            for i in range(len(reader1.pages)):
                rect = reader1.pages[i].cropbox
                x0, y0, x1, y1 = rect
                ut.print_info(f'Page {i}: {rect.width:.0f}x{rect.height:.0f}')

                if horizontal:
                    mid_y = (y0 + y1) / 2
                    half = RectangleObject((x0, y0, x1, mid_y))
                else:
                    mid_x = (x0 + x1) / 2
                    half = RectangleObject((x0, y0, mid_x, y1))

                set_page_boxes(reader1.pages[i], half)
                all_page.add_page(reader1.pages[i])

        with open(input_file, 'rb') as fp:
            reader2 = PdfReader(fp)
            for i in range(len(reader2.pages)):
                rect = reader2.pages[i].cropbox
                x0, y0, x1, y1 = rect

                if horizontal:
                    mid_y = (y0 + y1) / 2
                    half = RectangleObject((x0, mid_y, x1, y1))
                else:
                    mid_x = (x0 + x1) / 2
                    half = RectangleObject((mid_x, y0, x1, y1))

                set_page_boxes(reader2.pages[i], half)
                all_page.add_page(reader2.pages[i])

        with open(output_file, 'wb') as fo:
            all_page.write(fo)
        ut.print_info(f'Page-cut PDF saved: {output_file}')

    @staticmethod
    def to_png(input_file, output_dir, zoom=0.5):
        pdf_doc = fitz.open(input_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for pg in range(pdf_doc.page_count):
            page = pdf_doc[pg]
            mat = fitz.Matrix(zoom, zoom).prerotate(0)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            pix._writeIMG(os.path.join(output_dir, f'images_{pg}.png'), 1, 'ultra_high')
        ut.print_info(f'{pdf_doc.page_count} page(s) -> PNG under {output_dir}')
        pdf_doc.close()

    @staticmethod
    def to_txt(input_file, output_file):
        ut.print_info(f'Extracting text: {input_file}')
        doc = fitz.open(input_file)
        extracted = ""
        for page in doc:
            extracted += page.get_text()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted)
        doc.close()
        ut.print_info(f'Text saved: {output_file}')

    @staticmethod
    def images_to_pdf(image_paths, output_file):
        images = [Image.open(img).convert('RGB') for img in image_paths]
        images[0].save(output_file, save_all=True, append_images=images[1:])
        ut.print_info(f'PDF saved: {output_file}')

    @staticmethod
    def capture_word_cards(input_file, output_file, image_dir='png', keep_temp=False):
        def extract_images(pdf_path, img_path):
            total_pg = 0
            for f in pdf_path.split():
                ut.print_info('Analysis pdf file:', f)
                pdf_doc = fitz.open(f)
                for pg in range(pdf_doc.page_count):
                    if pg % 10 == 0:
                        ut.print_info('Check page:', pg)
                    page = pdf_doc[pg]
                    mat = fitz.Matrix(3, 3).prerotate(0)
                    for i in range(5):
                        grid = 145
                        x1, x2 = 10, 101
                        y1 = 88 + grid * i
                        y2 = y1 + (180 - 88)
                        clip = fitz.Rect(x1, y1, x2, y2)
                        pix = page.get_pixmap(matrix=mat, alpha=False, clip=clip)
                        if not os.path.exists(img_path):
                            os.makedirs(img_path)
                        pix.save(f'{img_path}/{str(pg + total_pg).zfill(3)}_{str(i).zfill(3)}.png')
                total_pg += pdf_doc.page_count

        def compose_images(img_path, out_file, keep):
            IMAGE_SIZE_X, IMAGE_SIZE_Y = 273, 273
            IMAGE_ROW, IMAGE_COLUMN = 9, 6
            space_x, space_y = 6, 6
            margin_x, margin_y = 120, 70
            image_width = 1900
            image_height = int(image_width * pow(2, 0.5))

            names = [n for n in os.listdir(img_path) if os.path.splitext(n)[1] == '.png']
            random.shuffle(names)
            total = len(names)
            per_page = IMAGE_COLUMN * IMAGE_ROW
            total_page = (total + per_page - 1) // per_page

            idx = 0
            page_no = 1
            jpg_files = []

            while idx < total:
                to_image = Image.new('RGB', (image_width, image_height), 'white')
                save_path = f'final_{page_no}.jpg'
                for y in range(IMAGE_ROW):
                    for x in range(IMAGE_COLUMN):
                        if idx < total:
                            px = margin_x + x * IMAGE_SIZE_X + x * space_x
                            py = margin_y + y * IMAGE_SIZE_Y + y * space_y
                            img_f = os.path.join(img_path, names[idx])
                            to_image.paste(Image.open(img_f), (px, py))
                            idx += 1
                to_image.save(save_path)
                tag = f'-{page_no}/{total_page}-'
                PDFToolbox._add_page_number(save_path, tag)
                jpg_files.append(save_path)
                page_no += 1

            doc = fitz.open()
            for jpg in jpg_files:
                imgdoc = fitz.open(jpg)
                pdfbytes = imgdoc.convert_to_pdf()
                pdf_name = jpg + '.pdf'
                imgpdf = fitz.open(pdf_name, pdfbytes)
                doc.insert_pdf(imgpdf)
            doc.save(out_file)
            doc.close()

            if not keep:
                for jpg in jpg_files:
                    os.remove(jpg)

            return total_page

        if os.path.isdir(image_dir):
            shutil.rmtree(image_dir)
        for root, dirs, files in os.walk('.'):
            for fn in files:
                if fn.startswith('final_') and fn.endswith('.jpg'):
                    os.remove(fn)
        try:
            os.remove(output_file)
        except OSError:
            pass

        extract_images(input_file, image_dir)
        pg_cnt = compose_images(image_dir, output_file, keep_temp)

        if not keep_temp:
            shutil.rmtree(image_dir)

        ut.print_info(f'Word-card PDF saved: {output_file} ({pg_cnt} pages)')

    @staticmethod
    def _add_page_number(img_file, number):
        bk_img = cv2.imread(img_file)
        w = bk_img.shape[1]
        cv2.putText(bk_img, str(number),
                    (int(w / 2 - 80), int(bk_img.shape[0] - 30)),
                    cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.imwrite(img_file, bk_img)

    @staticmethod
    def capture_receipt(input_file=None, input_dir=None, verbose=False, output_file='summary.txt'):
        def seek_files(path):
            files = []
            for root, dirs, fns in os.walk(path):
                for fn in fns:
                    if fn.endswith('.pdf'):
                        files.append(os.path.join(root, fn))
            return files

        if input_dir:
            file_list = seek_files(input_dir)
        elif input_file:
            file_list = input_file.split()
        else:
            ut.print_error('Either input_file or input_dir is required')
            return

        total = 0
        prices = {}
        for receipt in file_list:
            ut.print_info('Parse file:', receipt)
            tables = camelot.read_pdf(receipt, shift_text=[''], strip_text='\n')
            table = tables[0].df
            clm = len(table.columns) - 1 if len(table.columns) == 6 else len(table.columns) - 2
            price_str = table[clm][2][1:]

            try:
                price = float(price_str)
            except ValueError:
                price = float(table[clm][2][5:])

            try:
                price = float(price)
            except (ValueError, TypeError):
                if verbose:
                    ut.print_info(f'{receipt} is new e-receipt format')
                price = float(re.findall(r'\d+\.?\d*', tables[0].df[3][2])[0])

            total += price
            prices[receipt] = price

        with open(output_file, 'w', encoding='utf-8') as fo:
            fo.write(f'{"file":<60}{"price":>20}\n')
            fo.write('-' * 140 + '\n')
            for n in sorted(prices.keys()):
                fo.write(f'{n:<60}{prices[n]:>20}\n')
            fo.write('=' * 140 + '\n')
            fo.write(f'{len(prices):<60}{total:>20}\n')

        ut.print_info(f'Receipts: {len(prices)}, Total: {total}, Detail: {output_file}')
        return prices, total


EXAMPLES = '''
Examples:
  rotate   python pdf_toolbox.py rotate -i input.pdf -r 90 -o output.pdf
  merge    python pdf_toolbox.py merge -i a.pdf b.pdf -o merged.pdf
  split    python pdf_toolbox.py split -i input.pdf -o out_dir -g 2
  cut      python pdf_toolbox.py cut -i input.pdf -o output.pdf
           python pdf_toolbox.py cut -i input.pdf -o output.pdf -z   (horizontal)
  png      python pdf_toolbox.py png -i input.pdf -o imgs -z 0.5
  txt      python pdf_toolbox.py txt -i input.pdf -o output.txt
  img2pdf  python pdf_toolbox.py img2pdf -i 1.jpg 2.jpg -o output.pdf
  capture  python pdf_toolbox.py capture -i 1-200.pdf -o combined.pdf
  receipt  python pdf_toolbox.py receipt -f receipt.pdf
           python pdf_toolbox.py receipt -p ./pdf_folder
'''


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=scr_des_detail,
        epilog=EXAMPLES)
    sub = parser.add_subparsers(dest='command', help='Available commands')

    # rotate
    p = sub.add_parser('rotate', help='Rotate PDF pages',
                       description='Rotate all pages of a PDF clockwise by 90/180/270 degrees.\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-i', '--in_file', required=True, help='input PDF file')
    p.add_argument('-r', '--rotation', type=int, required=True, choices=[90, 180, 270],
                   help='rotation degree clockwise')
    p.add_argument('-o', '--out_file', required=True, help='output PDF file')

    # merge
    p = sub.add_parser('merge', help='Merge multiple PDFs',
                       description='Merge multiple PDF files into one.\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-i', '--in_files', nargs='+', required=True, help='input PDF file(s)')
    p.add_argument('-o', '--out_file', default='merged.pdf', help='output PDF file (default: merged.pdf)')

    # split
    p = sub.add_parser('split', help='Split PDF by page range',
                       description='Split a PDF into smaller files by page range.\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-i', '--in_file', required=True, help='input PDF file')
    p.add_argument('-o', '--out_folder', default='pdf_split', help='output folder (default: pdf_split)')
    p.add_argument('-s', '--start', type=int, help='start page (default: 1)')
    p.add_argument('-e', '--end', type=int, help='end page (default: last page)')
    p.add_argument('-g', '--grid', type=int, default=1, help='pages per split file (default: 1)')

    # cut
    p = sub.add_parser('cut', help='Cut each page in half (vertical or horizontal)',
                       description='Split each PDF page in half. Default: vertical (left/right).\n'
                       'Use -z for horizontal (top/bottom).\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-i', '--in_file', required=True, help='input PDF file')
    p.add_argument('-o', '--out_file', required=True, help='output PDF file')
    p.add_argument('-z', '--horizontal', action='store_true',
                   help='cut horizontally (top/bottom) instead of vertically')

    # png
    p = sub.add_parser('png', help='Convert PDF to PNG images',
                       description='Convert each PDF page into a PNG image file.\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-i', '--in_file', required=True, help='input PDF file')
    p.add_argument('-o', '--out_dir', default='imgs', help='output image directory (default: imgs)')
    p.add_argument('-z', '--zoom', type=float, default=0.5, help='zoom ratio (default: 0.5)')

    # txt
    p = sub.add_parser('txt', help='Extract text from PDF',
                       description='Extract text content from a PDF and save as TXT.\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-i', '--in_file', required=True, help='input PDF file')
    p.add_argument('-o', '--out_file', default='output.txt', help='output TXT file (default: output.txt)')

    # img2pdf
    p = sub.add_parser('img2pdf', help='Convert images to PDF',
                       description='Merge multiple image files (JPG/PNG) into a single PDF.\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-i', '--in_files', nargs='+', required=True, help='input image file(s)')
    p.add_argument('-o', '--out_file', default='output.pdf', help='output PDF file (default: output.pdf)')

    # capture
    p = sub.add_parser('capture', help='Capture word cards from PDF',
                       description='Extract word card regions from HongEn PDF and compose into a combined PDF.\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-i', '--in_file', default='./1-200.pdf', help='input PDF file (default: ./1-200.pdf)')
    p.add_argument('-o', '--out_file', default='./combined.pdf', help='output PDF file (default: ./combined.pdf)')
    p.add_argument('-k', '--keep_temp', action='store_true', help='keep temporary files')

    # receipt
    p = sub.add_parser('receipt', help='Extract fee from e-receipt PDFs',
                       description='Extract total fee amounts from Chinese tax e-receipt PDFs.\n' + EXAMPLES,
                       formatter_class=argparse.RawTextHelpFormatter)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', type=str, help='input PDF file(s) space-separated')
    group.add_argument('-p', '--path', type=str, help='folder containing PDF files')
    p.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    p.add_argument('-o', '--out_file', default='summary.txt', help='output summary file (default: summary.txt)')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    if args.command == 'rotate':
        PDFToolbox.rotate(args.in_file, args.out_file, args.rotation)
    elif args.command == 'merge':
        PDFToolbox.merge(args.in_files, args.out_file)
    elif args.command == 'split':
        PDFToolbox.split(args.in_file, args.out_folder, args.start, args.end, args.grid)
    elif args.command == 'cut':
        PDFToolbox.page_cut_by_half(args.in_file, args.out_file, horizontal=args.horizontal)
    elif args.command == 'png':
        PDFToolbox.to_png(args.in_file, args.out_dir, args.zoom)
    elif args.command == 'txt':
        PDFToolbox.to_txt(args.in_file, args.out_file)
    elif args.command == 'img2pdf':
        PDFToolbox.images_to_pdf(args.in_files, args.out_file)
    elif args.command == 'capture':
        PDFToolbox.capture_word_cards(args.in_file, args.out_file, keep_temp=args.keep_temp)
    elif args.command == 'receipt':
        PDFToolbox.capture_receipt(
            input_file=args.file, input_dir=args.path,
            verbose=args.verbose, output_file=args.out_file)


if __name__ == '__main__':
    ut.RUN_STATUS = 'RUN'
    ut.header(add_msg='')
    main()
    ut.footer()
