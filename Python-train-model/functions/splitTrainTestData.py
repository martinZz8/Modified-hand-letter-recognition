import math
import random
from sklearn.utils import shuffle


# Note: Output data is only randomly generated, it isn't shuffled
def splitTrainTestData(data: list,
                       testDataFactor: float = 0.2,
                       randomSeedVal: int = -1,  # testDataFactor stands for percentage of test data for single letter
                       shuffleData: bool = True):
    if testDataFactor < 0.0 or testDataFactor > 1.0:
        raise Exception("'testDataFactor' has wrong value: is less than 0.0 or greater than 1.0")

    if randomSeedVal != -1:
        random.seed(randomSeedVal)

    XTrain, YTrain, XTest, YTest = [], [], [], []
    allDrawnTestIdxs = [[] for i in range(len(data))]

    for letterIdx, singleLetters in enumerate(data):
        numOfTestLetters = round(testDataFactor * len(singleLetters))
        # print(f"numOfTestLetters: {numOfTestLetters}; len(singleLetters): {len(singleLetters)}")

        drawnTestLetters = []
        drawnTestIdxs = []

        # Get idxs and letters for test. Omit it when "numOfTestLetters" is >= "len(singleLetters)"
        if numOfTestLetters < len(singleLetters):
            while len(drawnTestIdxs) < numOfTestLetters:
                randIdx = random.randint(0, len(singleLetters) - 1)

                if randIdx not in drawnTestIdxs:
                    drawnTestLetters.append(singleLetters[randIdx])
                    drawnTestIdxs.append(randIdx)

        if len(drawnTestLetters) > 0:
            # Push "drawnTestLetters" to "XTest" list
            XTest += drawnTestLetters

            # Push "letterIdx" to "YTest" list "numOfTestLetters" times
            YTest += [letterIdx for i in range(numOfTestLetters)]

            # Place "drawnTestLetters" into "allDrawnTestIdxs" - at index corresponded to specified letter
            allDrawnTestIdxs[letterIdx] = drawnTestIdxs

        # Push other letters to "XTrain" list and corresponding letter indexes into "YTrain"
        for i in range(len(singleLetters)):
            if i not in drawnTestIdxs:
                XTrain.append(singleLetters[i])
                YTrain.append(letterIdx)

    random_state_to_use = randomSeedVal if randomSeedVal != -1 else None
    if shuffleData:
        XTrain, YTrain = shuffle(XTrain, YTrain, random_state=random_state_to_use)
        XTest, YTest = shuffle(XTest, YTest, random_state=random_state_to_use)

    return XTrain, YTrain, XTest, YTest, allDrawnTestIdxs
