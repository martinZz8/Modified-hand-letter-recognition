from os.path import join, dirname, isfile
from datetime import datetime

from getNextResultFileName import getNextResultFileName


def convertListToStr(li: list, delimiter=", "):
    return "[" + delimiter.join(li) + "]"


def saveResultsToFile(recognitionResults: list,
                      accuracy: float,
                      numOfErrorTerminations: int,
                      numOfProperRecognitions: int,
                      usedOptions: str):
    # Get file path to save results
    fileNameToSave = getNextResultFileName()
    filePath = join(dirname(dirname(__file__)), "output", fileNameToSave)
    print(f"Result file: \"{fileNameToSave}\"")

    # Combine str to save
    currentDateStr = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    predictedResults = list(map(lambda x: x['predictedLetter'], recognitionResults))
    realResults = list(map(lambda x: x['realLetter'], recognitionResults))

    strToSave = f"Test performed in: {currentDateStr}\n" \
                f"usedOptions: {usedOptions}\n" \
                f"predictedResults: {convertListToStr(predictedResults)}\n" \
                f"realResults: {convertListToStr(realResults)}\n" \
                f"accuracy: {accuracy}%\n" \
                f"numOfErrorTerminations: {numOfErrorTerminations}\n" \
                f"numOfProperRecognitions: {numOfProperRecognitions}\n" \
                f"numOfImproperRecognitions: {len(predictedResults) - numOfErrorTerminations - numOfProperRecognitions}\n" \
                f"numOfAllRecognitions: {len(predictedResults)}"

    # Save combined str to file
    with open(filePath, "w") as f:
        f.write(strToSave)
