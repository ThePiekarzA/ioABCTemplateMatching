import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class Plot:
    xValues = []
    yValues = []

    xMin = 0
    xMax = 0

    def __init__(self, _xMax):
        self.xMax = _xMax

        self.fig = plt.figure()
        plt.ion()


    def drawPoint(self, _yVal):
        self.xValues.append(len(self.xValues) + 1)
        self.yValues.append(_yVal)

        #plt.clear()
        plt.plot(self.xValues, self.yValues, 'b')
        plt.pause(0.05)
        #plt.show()


