import sys
from os.path import dirname
from math import floor

sys.path.append(dirname(dirname(__file__)))
from exceptions.ErrorBlankTensor import ErrorBlankTensor


def calcAccuracy(recognitionResults, isPrint=True):
    numOfErrorTerminations = len(list(filter(lambda x: x['errorTermination'], recognitionResults)))
    numOfProperRecognitions = len(list(filter(lambda x: x['properClassify'], recognitionResults)))
    
    if (len(recognitionResults) > 0) and (len(recognitionResults) != numOfErrorTerminations):
        calcAcc = (floor((numOfProperRecognitions / (len(recognitionResults) - numOfErrorTerminations)) * 100) / 100) * 100 # in percetange value
    else:
        raise ErrorBlankTensor("Error - blank recognition results")

    if isPrint:
        print(f"numOfErrorTerminations: {numOfErrorTerminations}\n"
              f"numOfProperRecognitions: {numOfProperRecognitions}\n"
              f"numOfImproperRecognitions: {len(recognitionResults) - numOfErrorTerminations - numOfProperRecognitions}\n"
              f"numOfAllRecognitions: {len(recognitionResults)}\n"
              f"calcAcc: {calcAcc}%")

    return calcAcc, numOfErrorTerminations, numOfProperRecognitions
