from os import listdir, makedirs
from os.path import exists, join, isdir
import functools
import torch


def saveModelToFile(model: torch.nn.Module,
                    outputDirName: str,
                    partialModelName: str,
                    modelExtensionName: str,
                    statisticsStr: str = "",
                    addTestDataToSaveStr: str = ""):
    # Create outer folder if doesn't exist
    if not exists(outputDirName):
        makedirs(outputDirName)

    # Search for folder that has inside "partialModelName" variable content
    onlyInnerFolders = [f
                        for f in listdir(outputDirName)
                        if isdir(join(outputDirName, f)) and partialModelName in f
                        ]

    # Search for biggest number inside this folder
    biggestNum = None
    if len(onlyInnerFolders) > 0:
        folderNamesAndVersions = list(
            filter(
                lambda y: len(y) > 1 and y[1] != "",
                map(
                    lambda x: x.split(partialModelName),
                    onlyInnerFolders
                )
            )
        )

        if len(folderNamesAndVersions) > 0:
            folderVersionNumbers = list(map(lambda x: int(x[1]), folderNamesAndVersions))
            biggestNum = functools.reduce(lambda acc, x: x if x > acc else acc, folderVersionNumbers)

    # Determine number to use
    numToUse = 1
    if biggestNum is not None:
        numToUse = biggestNum + 1

    # Create folder for model
    combinedFolderName = partialModelName + str(numToUse)
    makedirs(join(outputDirName, combinedFolderName))

    # Save model to folder
    combinedModelName = combinedFolderName + modelExtensionName
    torch.save(model.state_dict(), join(outputDirName, combinedFolderName, combinedModelName))

    # Save params to txt file
    if statisticsStr != "":
        txtFileName = "statistics.txt"

        with open(join(outputDirName, combinedFolderName, txtFileName), "w") as file:
            file.write(statisticsStr)

    # Save additional data to file
    if addTestDataToSaveStr != "":
        txtFileName = "additionalTestData.txt"

        with open(join(outputDirName, combinedFolderName, txtFileName), "w") as file:
            file.write(addTestDataToSaveStr)

    return combinedFolderName
