import sys
from os import listdir
from os.path import dirname, isfile, join
from tqdm.auto import tqdm

sys.path.append(dirname(__file__))
from formatInlineSkeleton import formatInlineSkeleton


def loadData(useMediaPipe: bool,
             useShiftedData: bool,
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

    loadedSkeletons = [[] for i in range(len(availableLetters))]

    for idx, letter in enumerate(tqdm(availableLetters)):
        pathToLetters = join(pathToData, letter)

        onlyFiles = [f for f in listdir(pathToLetters) if isfile(join(pathToLetters, f))]

        loadedSingleLetterSkeletons = [[] for i in range(len(onlyFiles))]
        for idx2, fileName in enumerate(onlyFiles):
            with open(join(pathToLetters, fileName), "r") as file:
                fileContent = file.read()
                loadedSingleLetterSkeletons[idx2] = formatInlineSkeleton(fileContent)

        loadedSkeletons[idx] = loadedSingleLetterSkeletons

    return loadedSkeletons
