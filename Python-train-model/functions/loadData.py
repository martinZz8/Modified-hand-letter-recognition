import sys
from os import listdir
from os.path import dirname, isfile, join
from tqdm.auto import tqdm

sys.path.append(dirname(__file__))
from formatInlineSkeleton import formatInlineSkeleton


# Helper functions
# Get num of person from str
def getPersonNum(strToWork: str):
    splittedFileName = strToWork.split("_")

    if len(splittedFileName) == 2:
        firstPartWithNum = splittedFileName[0]
        splittedFirstPartWithNum = firstPartWithNum.split("P")

        if len(splittedFirstPartWithNum) == 2:
            numOfPerson = splittedFirstPartWithNum[1]

            if numOfPerson.isnumeric():
                return int(numOfPerson)
    return 0


def loadData(useMediaPipe: bool,
             useShiftedData: bool,
             versionOfDataset: int,
             availableLetters: list[str]):
    basePathName = "datasets"
    mediaPipePathName = "MediaPipe"
    openPosePathName = "OpenPose"
    normalPathName = "normal"
    shiftedPathName = "shifted"

    if useMediaPipe:
        if useShiftedData:
            pathToData = join(basePathName, shiftedPathName, mediaPipePathName)
        else:
            pathToData = join(basePathName, normalPathName, mediaPipePathName)
    else:
        if useShiftedData:
            pathToData = join(basePathName, shiftedPathName, openPosePathName)
        else:
            pathToData = join(basePathName, normalPathName, openPosePathName)

    pathToData = f"{pathToData}{versionOfDataset}" if versionOfDataset > 1 else pathToData

    loadedSkeletons = [[] for i in range(len(availableLetters))]

    for idx, letter in enumerate(tqdm(availableLetters)):
        pathToLetters = join(pathToData, letter)

        onlyFiles = [f for f in listdir(pathToLetters) if isfile(join(pathToLetters, f))]

        loadedSingleLetterSkeletons = [{"personNum": 0, "skeleton": []} for i in range(len(onlyFiles))]

        for idx2, fileName in enumerate(onlyFiles):
            personNum = getPersonNum(fileName)

            with open(join(pathToLetters, fileName), "r") as file:
                fileContent = file.read()
                inlineSkeleton = formatInlineSkeleton(fileContent)
                loadedSingleLetterSkeletons[idx2] = {
                    "personNum": personNum,
                    "skeleton": inlineSkeleton
                }
        loadedSkeletons[idx] = loadedSingleLetterSkeletons

    return loadedSkeletons
