from math import floor


def calcAccuracy(recognitionResults, isPrint=True):
    numOfErrorTerminations = len(list(filter(lambda x: x['errorTermination'], recognitionResults)))
    numOfProperRecognitions = len(list(filter(lambda x: x['properClassify'], recognitionResults)))
    calcAcc = (floor((numOfProperRecognitions / (len(recognitionResults) - numOfErrorTerminations)) * 100) / 100) * 100 # in percetange value

    if isPrint:
        print(f"numOfErrorTerminations: {numOfErrorTerminations}\n"
              f"numOfProperRecognitions: {numOfProperRecognitions}\n"
              f"numOfImproperRecognitions: {len(recognitionResults) - numOfErrorTerminations - numOfProperRecognitions}\n"
              f"numOfAllRecognitions: {len(recognitionResults)}\n"
              f"calcAcc: {calcAcc}%")

    return calcAcc, numOfErrorTerminations, numOfProperRecognitions
