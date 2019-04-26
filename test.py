from yolo import YOLO
from PIL import Image
img = Image.open("frame2.jpg")

model = YOLO()

##изображение
out = model.detect_image(img)

##видос(массив в строку весь возвращается - я поправлю)

res = detect_video(model,"1.avi")