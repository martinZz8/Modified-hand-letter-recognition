import random
from sklearn.utils import shuffle


# Note: Output data is only randomly generated, it isn't shuffled
def splitTrainTestData(data: list,
                       losoPersonTester: int,
                       testDataFactor: float = 0.2,
                       randomSeedVal: int = -1,  # testDataFactor stands for percentage of test data for single letter
                       shuffleData: bool = True):
    XTrain, YTrain, XTest, YTest = [], [], [], []
    allDrawnPersonNums = [[] for i in range(len(data))]

    # Determine, whether we randomly draw data (if "losoPersonTester" <= -1) or use all data as train except with "losoPersonTester" number, which stands for test data
    if losoPersonTester <= -1:
        if testDataFactor < 0.0 or testDataFactor > 1.0:
            raise Exception("'testDataFactor' has wrong value: is less than 0.0 or greater than 1.0")

        if randomSeedVal != -1:
            random.seed(randomSeedVal)

        for letterIdx, singleLetter in enumerate(data):
            numOfTestLetters = round(testDataFactor * len(singleLetter))
            # print(f"numOfTestLetters: {numOfTestLetters}; len(singleLetters): {len(singleLetters)}")

            drawnTestLetters = []
            drawnPersonNums = []

            # Get idxs and letters for test. Omit it when "numOfTestLetters" is >= "len(singleLetters)"
            if numOfTestLetters < len(singleLetter):
                while len(drawnPersonNums) < numOfTestLetters:
                    randIdx = random.randint(0, len(singleLetter) - 1)

                    if randIdx not in drawnPersonNums:
                        drawnTestLetters.append(singleLetter[randIdx]["skeleton"])
                        drawnPersonNums.append(singleLetter[randIdx]["personNum"])

            if len(drawnTestLetters) > 0:
                # Push "drawnTestLetters" to "XTest" list
                XTest += drawnTestLetters

                # Push "letterIdx" to "YTest" list "numOfTestLetters" times
                YTest += [letterIdx for i in range(numOfTestLetters)]

                # Place "drawnTestLetters" into "allDrawnTestIdxs" - at index corresponded to specified letter
                allDrawnPersonNums[letterIdx] = drawnPersonNums

            # Push other letters to "XTrain" list and corresponding letter indexes into "YTrain"
            for i in range(len(singleLetter)):
                if i not in drawnPersonNums:
                    XTrain.append(singleLetter[i]["skeleton"])
                    YTrain.append(letterIdx)

        random_state_to_use = randomSeedVal if randomSeedVal != -1 else None
        if shuffleData:
            XTrain, YTrain = shuffle(XTrain, YTrain, random_state=random_state_to_use)
            XTest, YTest = shuffle(XTest, YTest, random_state=random_state_to_use)
    else:
        for letterIdx, singleLetter in enumerate(data):
            for singleSkeletonDict in singleLetter:
                if singleSkeletonDict["personNum"] != losoPersonTester:
                    XTrain.append(singleSkeletonDict["skeleton"])
                    YTrain.append(letterIdx)
                else:
                    XTest.append(singleSkeletonDict["skeleton"])
                    YTest.append(letterIdx)
                    allDrawnPersonNums[letterIdx].append(singleSkeletonDict["personNum"])

    return XTrain, YTrain, XTest, YTest, allDrawnPersonNums
