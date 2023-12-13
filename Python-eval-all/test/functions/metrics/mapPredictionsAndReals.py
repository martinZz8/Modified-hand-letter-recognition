import sys
from os.path import dirname, join

sys.path.append(join(dirname(dirname(dirname(__file__))), "batch-scripts", "functions"))
from reduceBlankRecognitions import reduceBlankRecognitions
from mapRecognitionsToIndexes import mapRecognitionsToIndexes


def mapPredictionsAndReals(predictedResults: list, realResults: list):
    predictedResults, realResults = reduceBlankRecognitions(predictedResults, realResults)

    predictedResultsIdx = mapRecognitionsToIndexes(predictedResults)
    realResultsIdx = mapRecognitionsToIndexes(realResults)

    return predictedResultsIdx, realResultsIdx
