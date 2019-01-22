from algorithm import ABC
import cv2
import os, gc, time

# DO NOT TOUCH THIS PART
# test output directory
directory = os.path.dirname(os.path.abspath(__file__)) + "\\Test results\\"

if not os.path.exists(directory):
    os.makedirs(directory)

currentTestNumber = 0

for subdir, dirs, files in os.walk(directory):
    dirs = [int(i) for i in dirs]
    dirs.sort()
    for folder in dirs:
        currentTestNumber = int(folder) + 1

directory += str(currentTestNumber) + "\\"

if not os.path.exists(directory):
    os.makedirs(directory)

logFileName = "{}logFile.txt".format(directory)

f = open(logFileName, "w")

# YOU CAN EDIT THIS PART

# specify how many times algorithm will be run
iterationNumber = 20

# load ref image and object image
imgRefName = 'img/ref1.jpg'
imgObjName = 'img/obiekt6.jpg'

imgRef = cv2.imread(imgRefName)
imgObj = cv2.imread(imgObjName)

f.write("Test {} log".format(currentTestNumber))
f.write("\nTest will be executed {} times".format(iterationNumber))
f.write("\nReference image: {}\nObject image: {}\n".format(imgRefName, imgObjName))

fitnesses = []
iterations = []
times = []

print("Test output directory is {}".format(directory))

firtTime = True

for iter in range(iterationNumber):
    plotFileName = "{}fitnessPlot_{:03d}".format(directory, iter + 1)
    imageFileName = "{}endResult_{:03d}".format(directory, iter + 1)

    print("Executing test: {}".format(iter+1))

    # create an Algorithm instance with desired parameters
    alg = ABC(imgRef, imgObj, _SN=60, _MCN=20, _NS=imgObj.shape[0] // 10)

    # for test purposes set gui to true and turn on testmode, also show plot
    alg.settings(_showGUI=True, _testMode=True, _showPlot=True, _plotFileName=plotFileName, _imgFileName=imageFileName)

    if firtTime:
        f.write("\nAlgoritm settings:")
        f.write("\nSN {}".format(alg.SN))
        f.write("\nEBN {}".format(alg.EBN))
        f.write("\nMCN {}".format(alg.MCN))
        f.write("\nNS {}".format(alg.NS))
        f.write("\nNSN {}".format(alg.NSN))
        f.write("\nSLT {}".format(alg.SLT))

        f.write("\n")

        firtTime = False

    start = time.time()

    # run the algorithm
    alg.run()

    end = time.time()

    calculationTime = end - start
    times.append(calculationTime)

    fitnesses.append(alg.bestSolution.fitness)
    iterations.append(alg.bestSolutionIterationNumber)

    f.write("\nBest result found on iteration {} is ({}, {}, {}), fitness: {}, time: {:.02f}s".format(alg.bestSolutionIterationNumber,
                                                                                    alg.bestSolution.x,
                                                                                      alg.bestSolution.y,
                                                                                      alg.bestSolution.angle,
                                                                                      alg.bestSolution.fitness,
                                                                                          calculationTime))

    del alg

    gc.collect(2)

bestF = max(fitnesses)
worstF = min(fitnesses)
avgF = sum(fitnesses)/float(iterationNumber)

bestT = min(times)
worstT = max(times)
avgT = sum(times)/float(iterationNumber)

bestI = min(iterations)
worstI = max(iterations)
avgI = sum(iterations)/float(iterationNumber)

f.write("\n\nTest summary")
f.write("\nFitness best {}, worst {}, average, {}".format(bestF, worstF, avgF))
f.write("\nIterations best {}, worst {}, average, {}".format(bestI, worstI, avgI))
f.write("\nTime best {:.02f}s, worst {:.02f}s, average, {:.02f}s".format(bestT, worstT, avgT))

f.close()
