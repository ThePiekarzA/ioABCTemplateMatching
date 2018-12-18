from algorithm import ABC

import numpy as np
import cv2

# load ref image and object image
imgRef = cv2.imread('img/ref3.jpg')
imgObj = cv2.imread('img/obiekt3.jpg')

alg = ABC(imgRef, imgObj, _SN=20, _MCN=50)

alg.settings(_showGUI=True)

alg.run()

