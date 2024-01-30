from typing import Optional
from os import listdir
from os.path import dirname, join, isdir, isfile


# Helper funcs
def doesFolderContainsFiles(folderPath):
    return len([f for f in listdir(folderPath) if isfile(join(folderPath, f))]) > 0


# Export functions
def doesModelFolderExists(skeletonReceiver: str,
                          shiftParams: str,
                          personNum: Optional[int] = None,
                          modelVersion: Optional[int] = None):
    pathToOutputModelsDir = join(dirname(dirname(dirname(dirname(__file__)))), "outputModels")
    modelFolderName = f"HSRecModel_{f'LOSO_{personNum}_' if personNum is not None else ''}" \
                      f"{'M' if skeletonReceiver == '-m' else 'O'}" \
                      f"{'S' if shiftParams == 's' else 'O'}" \
                      f"{modelVersion if modelVersion is not None else ''}"
    pathToSpecificFolder = join(pathToOutputModelsDir, modelFolderName)

    # If modelVersion is not None, check whether exists and contains some values.
    if modelVersion is not None:
        return isdir(pathToSpecificFolder) and doesFolderContainsFiles(pathToSpecificFolder)

    # Else check for first occurrence of folder, that starts with name specified in "modelFolderName" variable. Also check if that folder contains some files.
    dirsInsideOutputModels = listdir(pathToOutputModelsDir)
    matchingInnerDirs = list(filter(lambda dName: dName.startswith(modelFolderName), dirsInsideOutputModels))

    return len(matchingInnerDirs) > 0 and doesFolderContainsFiles(join(pathToOutputModelsDir, matchingInnerDirs[0]))
