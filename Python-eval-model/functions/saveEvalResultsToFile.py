from os import listdir, makedirs
from os.path import exists, join, isfile
import functools


def saveEvalResultsToFile(outputDirName: str,
                          statisticsStr: str):
    outputFileName = "results"
    outputFileExtensionName = ".txt"

    # Create outer folder if doesn't exist
    if not exists(outputDirName):
        makedirs(outputDirName)

    # Search for files that has inside "outputFileName" variable content
    onlyInnerFiles = [f
                      for f in listdir(outputDirName)
                      if isfile(join(outputDirName, f)) and outputFileName in f
                      ]

    # Search for biggest number inside this folder
    biggestNum = None
    if len(onlyInnerFiles) > 0:
        fileVersionsAndExtensions = list(
            filter(
                lambda y: len(y) > 1 and y[0] != "",
                map(
                    lambda x: x.split(outputFileName)[1].split("."),
                    onlyInnerFiles
                )
            )
        )

        if len(fileVersionsAndExtensions) > 0:
            fileVersionNumbers = list(map(lambda x: int(x[0]), fileVersionsAndExtensions))
            biggestNum = functools.reduce(lambda acc, x: x if x > acc else acc, fileVersionNumbers)

    # Determine number to use
    numToUse = 1
    if biggestNum is not None:
        numToUse = biggestNum + 1

    # Combine file name
    combinedFileName = outputFileName + str(numToUse) + outputFileExtensionName

    # Save statistics to txt file
    if statisticsStr != "":
        with open(join(outputDirName, combinedFileName), "w") as file:
            file.write(statisticsStr)

    return combinedFileName
