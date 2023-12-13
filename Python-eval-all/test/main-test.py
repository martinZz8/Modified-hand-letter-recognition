# Standard imports
import sys
from tqdm.auto import tqdm
from os.path import dirname, join
from timeit import default_timer as timer

# Custom functions imports
from functions.getArgumentOptionsTest import getArgumentOptionsTest
from functions.loadImagePaths import loadImagePaths
from functions.performTest import performTest
from functions.metrics.calcAccuracy import calcAccuracy
from functions.metrics.calcPrecision import calcPrecision
from functions.metrics.calcRecall import calcRecall
from functions.metrics.calcF1Score import calcF1Score
from functions.saveResultsToFile import saveResultsToFile

# Custom consts imports
from consts.consts import combinedOptions

# Custom exceptions imports
from exceptions.ErrorMismatchResultLen import ErrorMismatchResultLen
from exceptions.ErrorBlankTensor import ErrorBlankTensor


def main(argv):
    # -- Consts (for eval model function) --

    # --Option variables--
    selectedOptionIdx = 0  # default: 0
    inputImagesFolderPath: str = join(dirname(__file__), "input", "images")  # default: "<curr_workdir_path>/input/images"
    useCuda: bool = False  # default: False

    # --Read input arguments and set variables--
    selectedOptionIdx, inputImagesFolderPath, useCuda = getArgumentOptionsTest(argv,
                                                                               selectedOptionIdx,
                                                                               inputImagesFolderPath,
                                                                               useCuda)

    # Terminate script, when "selectedOptionIdx" is out of range <0,11>
    if (selectedOptionIdx < 0) or (selectedOptionIdx > (len(combinedOptions)-1)):
        print("Error during passing 'selectedOptionIdx' argument, it has to be in range of <0,11>")
        sys.exit(1)

    # --Load image paths (list of dictionaries)--
    print(f"1. Getting images paths ...")
    loadedImagePaths = loadImagePaths(inputImagesFolderPath)

    # --Performing recognitions--
    print(f"2. Performing recognitions ...")

    # Start the timer
    evalTimeStart = timer()

    # Perform recognitions
    recognitionResults = []
    for idx, imagePath in enumerate(tqdm(loadedImagePaths)):
        resultOfTest = performTest(selectedOptionIdx, imagePath)

        recognitionResults.append({
            'imageFileName': imagePath['imageFileName'],
            'errorTermination': resultOfTest['errorTermination'],
            'realLetter': resultOfTest['realLetter'],
            'predictedLetter': resultOfTest['predictedLetter'],
            'properClassify': resultOfTest['properClassify']
        })

    # Stop the timer
    evalTimeStop = timer()

    # Count elapsed time
    elapsedTime = evalTimeStop - evalTimeStart

    # --Calc accuracy and other params of results--
    print(f"3. Calculating accuracy and other params ...")
    if len(recognitionResults) > 0:
        calcedAcc, numOfErrorTerminations, numOfProperRecognitions = calcAccuracy(recognitionResults)

        try:
            calcedPrecision = calcPrecision(recognitionResults)
            calcedRecall = calcRecall(recognitionResults)
            calcedF1Score = calcF1Score(recognitionResults)
        except (ErrorMismatchResultLen, ErrorBlankTensor) as e:
            print(f"{e} Terminated script.")
            sys.exit(1)

        # --Save results to file--
        print(f"4. Saving results to output file ...")
        saveResultsToFile(recognitionResults,
                          calcedAcc,
                          calcedPrecision,
                          calcedRecall,
                          calcedF1Score,
                          elapsedTime,
                          numOfErrorTerminations,
                          numOfProperRecognitions,
                          combinedOptions[selectedOptionIdx])


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF 'main-test.py' SCRIPT --")
