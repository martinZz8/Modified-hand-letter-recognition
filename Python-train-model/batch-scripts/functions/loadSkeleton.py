import sys
from os.path import dirname, join, isfile

sys.path.append(join(dirname(dirname(dirname(__file__))), "functions"))
from formatInlineSkeleton import formatInlineSkeleton


def loadSkeleton(pathToInputFile: str) -> list:
    if isfile(pathToInputFile):
        with open(pathToInputFile, "r") as file:
            fileContent = file.read()
            loadedSkeleton = formatInlineSkeleton(fileContent)
    else:
        raise Exception("Input file doesn't exist in input folder.")

    return loadedSkeleton
