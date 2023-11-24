from os import listdir
from os.path import isfile, join
from tqdm.auto import tqdm


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
                fileContentLines = list(filter(lambda x: len(x) > 0, fileContent.split("\n")))
                fileContentLinesSplitted = list(
                    map(
                        lambda x: list(
                            map(
                                lambda y: float(y),
                                x.split(" ")
                            )
                        ),
                        fileContentLines
                    )
                )

                loadedSingleLetterSkeletons[idx2] = fileContentLinesSplitted

        loadedSkeletons[idx] = loadedSingleLetterSkeletons

    return loadedSkeletons
