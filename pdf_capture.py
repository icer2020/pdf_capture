import sys
import fitz
import os
import datetime
import random
import PIL.Image as Image

 
def pyMuPDF2_fitz(pdfPath, imagePath):
    pdfDoc = fitz.open(pdfPath) # open document
    for pg in range(pdfDoc.page_count): # iterate through the pages
        print("-I- check page: ", pg)
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate) # 缩放系数1.3在每个维度  .prerotate(rotate)是执行一个旋转
        rect = page.rect                         # 页面大小

        mp = rect.tl + (rect.bl - (0,75/zoom_x)) # 矩形区域    56=75/1.3333
        clip = fitz.Rect(mp, rect.br)            # 想要截取的区域
        print("rect:", rect)
        # print("clip:", clip)
        # print("mp:", mp)
        # print("rect.br:", rect.br)
        clip = rect
        
        # clip = fitz.Rect(10, 88, 101, 180)            # golden for 1st word
        x1 = 10
        x2 = x1 + 91
        y1 = 88
        y2 = y1 + (180-88)
        # clip = fitz.Rect(x1, y1, x2, y2)            # golden for 1st word
        grid = 145
        x1 = 10
        x2 = x1 + 91
        y1 = 88 + grid
        # y1 = 88 
        y2 = y1 + (180-88)
        clip = fitz.Rect(x1, y1, x2, y2)            # golden for 1st word

        j = 0
        for i in range(5):
            grid = 145
            x1 = 10
            x2 = x1 + 91
            y1 = 88 + grid*i
            # y1 = 88 
            y2 = y1 + (180-88)
            clip = fitz.Rect(x1, y1, x2, y2)            # golden for 1st word
            pix = page.get_pixmap(matrix=mat, alpha=False, clip=clip) # 将页面转换为图像
            if not os.path.exists(imagePath):
                os.makedirs(imagePath)
            # pix.writePNG(imagePath+'/'+'psReport_%s.png' % pg)# store image as a PNG
            pix.save(f'{imagePath}/{pg}_{i}.png')

   
def image_compose():
    IMAGES_PATH = imagePath
    IMAGES_FORMAT = ['.png']  # 图片格式
    IMAGE_SIZE_X = 91  # 每张小图片的大小
    IMAGE_SIZE_Y = 92  # 每张小图片的大小
    IMAGE_ROW = 9  # 图片间隔，也就是合并成一张图后，一共有几行
    IMAGE_COLUMN = 6  # 图片间隔，也就是合并成一张图后，一共有几列
    IMAGE_SAVE_PATH = 'final.jpg'  # 图片转换后的地址
    space_x = 3
    space_y = 3
    margin_x = 25
    margin_y = 5
    # 获取图片集地址下的所有图片名称
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if os.path.splitext(name)[1] == item]
    # to_image = Image.new('RGB', ( (IMAGE_COLUMN*IMAGE_SIZE_X)+space_x*(IMAGE_COLUMN-1) , (IMAGE_ROW*IMAGE_SIZE_Y)+space_y*(IMAGE_ROW-1)) #创建一个新图
    
    # print(len(image_names))

    image_width = 610
    image_height = int(image_width * pow(2, 0.5))
    random.shuffle(image_names)
    # print(image_names)

    
    to_image = Image.new('RGB', (image_width, image_height), "white")
    img_cnt = 0
    for y in range(IMAGE_ROW):
        for x in range(IMAGE_COLUMN):
            point_x = margin_x + x*IMAGE_SIZE_X + x*space_x 
            point_y = margin_y + y*IMAGE_SIZE_Y + y*space_y
            img_f = IMAGES_PATH + "/" + image_names[img_cnt] 
            print("point_x: {:} point_y: {:}".format(point_x, point_y))
            to_image.paste(Image.open(img_f), (point_x, point_y))
            img_cnt += 1
    return to_image.save(IMAGE_SAVE_PATH) # 保存新图



if __name__ == "__main__":
    pdfPath = '1-200.pdf'
    # pdfPath = '201-600.pdf'
    imagePath = 'png'
    # pyMuPDF2_fitz(pdfPath, imagePath)#指定想要的区域转换成图片
    image_compose()