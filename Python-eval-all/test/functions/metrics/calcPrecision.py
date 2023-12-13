from torchmetrics import Precision


def calcPrecision(recognitionResults, isPrint=True):
    realResults = list(map(lambda x: x['realLetter'], recognitionResults))
    predictedResults = list(map(lambda x: x['predictedLetter'], recognitionResults))

    precisionObj = Precision(task="multiclass",
                             average='macro',
                             num_classes=len(recognitionResults))

    countedPrecision = precisionObj(predictedResults, realResults)

    if isPrint:
        print(f"countedPrecision: {countedPrecision}")

    return countedPrecision
