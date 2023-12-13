from os.path import join, dirname, isfile
from datetime import datetime

from getNextResultFileName import getNextResultFileName


def convertListToStr(li: list, delimiter=", "):
    return "[" + delimiter.join(li) + "]"


def saveResultsToFile(recognitionResults: list,
                      accuracy: float,
                      precision: float,
                      recall: float,
                      f1Score: float,
                      elapsedTime: float,
                      numOfErrorTerminations: int,
                      numOfProperRecognitions: int,
                      usedOptions: str):
    # Get file path to save results
    fileNameToSave = getNextResultFileName()
    filePath = join(dirname(dirname(__file__)), "output", fileNameToSave)

    # Combine str to save
    currentDateStr = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    predictedResults = list(map(lambda x: x['predictedLetter'], recognitionResults))
    realResults = list(map(lambda x: x['realLetter'], recognitionResults))

    strToSave = f"Test performed in: {currentDateStr}\n" \
                f"usedOptions: {usedOptions}\n" \
                f"predictedResults: {convertListToStr(predictedResults)}\n" \
                f"realResults: {convertListToStr(realResults)}\n" \
                f"accuracy: {accuracy}%\n" \
                f"precision: {precision}%\n" \
                f"recall: {recall}%\n" \
                f"f1Score: {f1Score}%\n" \
                f"elapsedTime(sec): {elapsedTime:.3f}%\n" \
                f"numOfErrorTerminations: {numOfErrorTerminations}\n" \
                f"numOfProperRecognitions: {numOfProperRecognitions}\n" \
                f"numOfImproperRecognitions: {len(predictedResults) - numOfErrorTerminations - numOfProperRecognitions}\n" \
                f"numOfAllRecognitions: {len(predictedResults)}"

    # Save combined str to file
    with open(filePath, "w") as f:
        f.write(strToSave)

    print(f"Result saved to file: \"{fileNameToSave}\"")
