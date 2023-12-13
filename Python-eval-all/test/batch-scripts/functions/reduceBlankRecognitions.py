import sys
from os.path import dirname

sys.path.append(dirname(dirname(__file__)))
from exceptions.ErrorMismatchResultLen import ErrorMismatchResultLen


def reduceBlankRecognitions(predictedResults: list, realResults: list):
    newPredictedResults = []
    newRealResults = []

    if len(predictedResults) == len(realResults):
        for i in range(len(predictedResults)):
            if predictedResults[i] != "-":
                newPredictedResults.append(predictedResults[i])
                newRealResults.append(realResults[i])

        # Or instead write:
        """
        nn = len(predictedResults)
        i = 0
        while i < nn:
            if predictedResults[i] == "-":
                del predictedResults[i]
                del realResults[i]
                i -= 1
                nn -= 1
            i += 1
        """
        # Then we return predictedResults, realResults
    else:
        raise ErrorMismatchResultLen("Error - lengths of lists \"predictedResults\" and \"realResults\" doesn't match")

    return newPredictedResults, newRealResults
