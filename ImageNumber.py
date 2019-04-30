from PIL import Image,ImageOps
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#im = Image.open("frame_Cam4_2018-09-25_08.00.01.jpg")
im = Image.open('frame_9013-423_2019-04-05_09.34.12.jpg')
im=ImageOps.invert(im)
im = im.convert("P")
im2 = Image.new("P",im.size,255)

im = im.convert("P")

temp = {}

for x in range(im.size[1]):
  for y in range(im.size[0]):
    pix = im.getpixel((y,x))
    temp[pix] = pix
    if pix == 0 : # these are the numbers to get
      im2.putpixel((y,x),0)

im2.save("output.png")
text = pytesseract.image_to_string(im2)
print(text)