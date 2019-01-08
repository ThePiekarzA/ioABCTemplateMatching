from algorithm import ABC

import numpy as np
import cv2

# load ref image and object image
imgRef = cv2.imread('img/ref1.jpg')
imgObj = cv2.imread('img/obiekt6.jpg')

alg = ABC(imgRef, imgObj, _SN=40, _MCN=50, _NS=imgObj.shape[0]//10)

alg.settings(_showGUI=True, _showPlot=True)

alg.run()

