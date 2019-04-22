import cv2
import matplotlib.pyplot as plt
import numpy as np
try:
    from pathlib import Path
except ImportError:             # Python 2
    from pathlib2 import Path
p = Path('/Users/maksimpolakov/PycharmProjects/untitled/venv/frames')

# читаем кадры
imgs = [cv2.imread(str(f)) for f in p.glob('*.jpg')]
#plt.imshow(imgs[10])
#plt.show()
# создаем видео
width,height, layers = imgs[0].shape
#print(height)
#print(width)
fps = 1
capSize = (height,width) # this is the size of my source video
fourcc = cv2.VideoWriter_fourcc(*'m', 'p', '4', 'v') # note the lower case
vout = cv2.VideoWriter()
success = vout.open('output.avi',fourcc,fps,capSize,True)
_=[vout.write(i) for i in imgs]
cv2.destroyAllWindows()
vout.release()

