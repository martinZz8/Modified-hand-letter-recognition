from os.path import join, dirname, isdir, isfile
import torch


def loadModelObject(useMediaPipe: bool,
                    useShiftedData: bool,
                    modelVersion: int):
    # Specify path to model folders
    pathToModelFolders = join(
        dirname(
            dirname(
                (dirname(__file__))
            )
        ),
        "Python-train-model", "outputModels"
    )

    # Specify model folder name
    modelObjectFolderName = "HSRecModel_"

    if useMediaPipe:
        modelObjectFolderName += "M"
    else:
        modelObjectFolderName += "O"

    if useShiftedData:
        modelObjectFolderName += "S"
    else:
        modelObjectFolderName += "O"

    modelObjectFolderName += str(modelVersion)

    # Specify model name
    modelObjectName = modelObjectFolderName + ".pth"

    # Change whether desired model exists
    desiredDirPath = join(pathToModelFolders, modelObjectFolderName)
    if isdir(desiredDirPath):
        desiredFilePath = join(desiredDirPath, modelObjectName)

        if isfile(desiredFilePath):
            # Read model
            savedModelObject = torch.load(desiredFilePath)
        else:
            raise Exception(f"There is no model object named '{modelObjectName}' inside '{modelObjectFolderName}' folder")
    else:
        raise Exception(f"There is no folder named '{modelObjectFolderName}'")

    return savedModelObject, modelObjectFolderName
