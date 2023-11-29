from os.path import join, isfile
from functions.formatInlineSkeleton import formatInlineSkeleton


def loadInputSkeleton(folderName: str,
                      fileName: str) -> list:
    pathToInputFile = join(folderName, fileName)

    if isfile(pathToInputFile):
        with open(pathToInputFile, "r") as file:
            fileContent = file.read()
            loadedSkeleton = formatInlineSkeleton(fileContent)
    else:
        raise Exception("Input file doesn't exist in input folder.")

    return loadedSkeleton
