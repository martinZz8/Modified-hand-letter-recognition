from torchmetrics import Recall


def calcRecall(recognitionResults, isPrint=True):
    realResults = list(map(lambda x: x['realLetter'], recognitionResults))
    predictedResults = list(map(lambda x: x['predictedLetter'], recognitionResults))

    recallObj = Recall(task="multiclass",
                       average='macro',
                       num_classes=len(recognitionResults))

    countedRecall = recallObj(predictedResults, realResults)

    if isPrint:
        print(f"countedRecall: {countedRecall}")

    return countedRecall
