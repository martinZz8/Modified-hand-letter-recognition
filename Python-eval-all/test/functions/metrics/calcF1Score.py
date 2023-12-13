import sys
from os.path import dirname
import torch
from torchmetrics import F1Score

sys.path.append(dirname(dirname(__file__)))
from metrics.mapPredictionsAndReals import mapPredictionsAndReals
from exceptions.ErrorBlankTensor import ErrorBlankTensor


def calcF1Score(recognitionResults, isPrint=True):
    realResults = list(map(lambda x: x['realLetter'], recognitionResults))
    predictedResults = list(map(lambda x: x['predictedLetter'], recognitionResults))

    predictedResultsIdx, realResultsIdx = mapPredictionsAndReals(predictedResults, realResults)
    predictedResultsIdxTensor, realResultsIdxTensor = torch.tensor(predictedResultsIdx), torch.tensor(realResultsIdx)

    if len(predictedResultsIdxTensor) > 0:
        f1ScoreObj = F1Score(task="multiclass",
                             average='macro',
                             num_classes=len(recognitionResults))

        countedF1Score = f1ScoreObj(predictedResultsIdxTensor, realResultsIdxTensor)

        if isPrint:
            print(f"countedF1Score: {countedF1Score}")
    else:
        raise ErrorBlankTensor("Error - blank tensors")

    return countedF1Score
