from os import listdir, makedirs
from os.path import exists, join, isfile
import functools


def saveEvalResultsToFile(prefOutputDirName: str,
                          prefOutputFileNameWithExt: str,
                          statisticsStr: str):
    # Create outer folder if doesn't exist
    if not exists(prefOutputDirName):
        makedirs(prefOutputDirName)

    # Search for files that has inside "outputFileName" variable content - if "prefOutputFileNameWithExt" is blank
    if len(prefOutputFileNameWithExt) == 0:
        outputFileName = "results"
        outputFileExtensionName = ".txt"

        onlyInnerFiles = [f
                          for f in listdir(prefOutputDirName)
                          if isfile(join(prefOutputDirName, f)) and outputFileName in f
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
    else:
        combinedFileName = prefOutputFileNameWithExt

    # Save statistics to txt file
    if statisticsStr != "":
        with open(join(prefOutputDirName, combinedFileName), "w") as file:
            file.write(statisticsStr)

    return combinedFileName
