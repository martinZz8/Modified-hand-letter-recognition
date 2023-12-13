import sys
from os.path import dirname
import torch
from torchmetrics import Precision

sys.path.append(dirname(dirname(__file__)))
from metrics.mapPredictionsAndReals import mapPredictionsAndReals
from exceptions.ErrorBlankTensor import ErrorBlankTensor

def calcPrecision(recognitionResults, isPrint=True):
    realResults = list(map(lambda x: x['realLetter'], recognitionResults))
    predictedResults = list(map(lambda x: x['predictedLetter'], recognitionResults))

    predictedResultsIdx, realResultsIdx = mapPredictionsAndReals(predictedResults, realResults)
    predictedResultsIdxTensor, realResultsIdxTensor = torch.tensor(predictedResultsIdx), torch.tensor(realResultsIdx)

    if len(predictedResultsIdxTensor) > 0:
        precisionObj = Precision(task="multiclass",
                                 average='macro',
                                 num_classes=len(recognitionResults))

        countedPrecision = precisionObj(predictedResultsIdxTensor, realResultsIdxTensor)

        if isPrint:
            print(f"countedPrecision: {countedPrecision}")
    else:
        raise ErrorBlankTensor("Error - blank tensors")

    return countedPrecision
