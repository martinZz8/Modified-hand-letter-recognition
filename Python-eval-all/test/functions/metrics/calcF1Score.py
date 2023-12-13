from torchmetrics import F1Score


def calcF1Score(recognitionResults, isPrint=True):
    realResults = list(map(lambda x: x['realLetter'], recognitionResults))
    predictedResults = list(map(lambda x: x['predictedLetter'], recognitionResults))

    f1ScoreObj = F1Score(task="multiclass",
                         average='macro',
                         num_classes=len(recognitionResults))

    countedF1Score = f1ScoreObj(predictedResults, realResults)

    if isPrint:
        print(f"countedF1Score: {countedF1Score}")

    return countedF1Score
