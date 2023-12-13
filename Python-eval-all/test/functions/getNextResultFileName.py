from os.path import join, dirname, isfile
from os import listdir


def isFileNameProper(baseFileName, fileNameToCompare):
    splittedBaseFileName = baseFileName.split(".")
    splittedFileNameToCompare = fileNameToCompare.split(".")
    splittedFileNameToCompare2 = splittedFileNameToCompare[0].split("_")

    if len(splittedFileNameToCompare2) > 1:
        if splittedBaseFileName[0] == splittedFileNameToCompare2[0]:
            if splittedBaseFileName[1] == splittedFileNameToCompare[1]:
                return True
    return False


def combineNextFileName(baseFileName, num):
    splittedBaseFileName = baseFileName.split(".")
    splittedBaseFileName2 = splittedBaseFileName[0].split("_")

    return splittedBaseFileName2[0] + "_" + str(num) + "." + splittedBaseFileName[1]


# Get next result file name based on current result files located in "output" folder.
# E.g last fle name is "results_1.txt", next would be "results_2.txt"
def getNextResultFileName(baseFileName="results.txt"):
    # Get all result file names
    pathToOutputFolder = join(dirname(dirname(__file__)), "output")
    fileNames = [f for f in listdir(pathToOutputFolder) if isfile(join(pathToOutputFolder, f))]
    filteredFileNames = list(filter(lambda x: isFileNameProper(baseFileName, x), fileNames))

    # Determine biggest and next nums
    biggestNum = 0

    for fileName in filteredFileNames:
        fileNumStr = fileName.split(".")[0].split("_")[1]

        if fileNumStr.isnumeric():
            fileNum = int(fileNumStr)

            if fileNum > biggestNum:
                biggestNum = fileNum

    nextNum = biggestNum + 1

    return combineNextFileName(baseFileName, nextNum)
