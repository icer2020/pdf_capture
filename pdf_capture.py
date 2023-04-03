import sys
import fitz
import os
import datetime
import PIL.Image as Image

 
def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()#开始时间
    
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.page_count):
        print("-I- check page: ", pg)
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建
        
        pix._writeIMG(imagePath+'/'+'images_%s.png' % pg)#将图片写入指定的文件夹内
        
    endTime_pdf2img = datetime.datetime.now()#结束时间
    print('pdf2img时间=',(endTime_pdf2img - startTime_pdf2img).seconds)
 
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
        # print("rect:", rect)
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
'''
import PIL.Image as Image
import os
 
IMAGES_PATH = 'E:\picture\新垣结衣\\'  # 图片集地址
IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
IMAGE_SIZE = 256  # 每张小图片的大小
IMAGE_ROW = 4  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 4  # 图片间隔，也就是合并成一张图后，一共有几列
IMAGE_SAVE_PATH = 'E:\\picture\\新垣结衣\\final.jpg'  # 图片转换后的地址
 
# 获取图片集地址下的所有图片名称
image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
               os.path.splitext(name)[1] == item]
 
# 简单的对于参数的设定和实际图片集的大小进行数量判断
if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
    raise ValueError("合成图片的参数和要求的数量不能匹配！")
 
# 定义图像拼接函数
def image_compose():
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) #创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                (IMAGE_SIZE, IMAGE_SIZE),Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
    return to_image.save(IMAGE_SAVE_PATH) # 保存新图
image_compose() #调用函数

'''



if __name__ == "__main__":
    # pdfPath = '1-200.pdf'
    pdfPath = '201-600.pdf'
    imagePath = 'jpeg'
    #pyMuPDF_fitz(pdfPath, imagePath)#只是转换图片
    pyMuPDF2_fitz(pdfPath, imagePath)#指定想要的区域转换成图片