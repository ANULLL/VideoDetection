from PIL import Image,ImageOps
import pytesseract
import datetime as dt


def nn_filter(n_file):
  b = False
  if (n_file[0] == '0' and len(n_file) == 19 and filter_date(n_file) and filter_time(n_file)):
    b = True
  return b
def filter_time(f):
  b=True
  hour = f[0:2:1]
  minute = f[3:5:1]
  second = f[6:8:1]
  try:
    d = dt.time(int(hour), int(minute), int(second))
  except ValueError:
    b=False
  return b
def filter_date(f):
  b=True
  day = f[9:11:1]
  month = f[12:14:1]
  year = f[15:len(f):1]
  try:
    d = dt.date(int(year), int(month), int(day))
  except ValueError:
    b=False
  return b
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#im = Image.open("frame_Cam4_2018-09-25_08.00.01.jpg")
im = Image.open('frame.Cam1_07.34.21_24.09.2018.jpg')
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
#text = pytesseract.image_to_string(im2)
text='07._a1_3_24.09.2018'
print(nn_filter(text))
print('len ',len(text))
print(type(text))
print(text)
remove = text[0:text.find('\n') + 1:1]
text = text.replace(remove, '')
text = text.replace(':', '.')
text = text.replace(' ', '_')
if (text.find('.') == 1):
  text = '0' + text
print(text)
d=filter_time(text)
print(d)
d=filter_date(text)
print(d)
