# Standard imports
import sys
from tqdm.auto import tqdm
from os.path import dirname, join

# Custom functions imports
from functions.getArgumentOptionsTest import getArgumentOptionsTest
from functions.loadImagePaths import loadImagePaths
from functions.performTest import performTest
from functions.calcAccuracy import calcAccuracy
from functions.saveResultsToFile import saveResultsToFile

# Custom consts imports
# sys.path.append(dirname(__file__))
from consts.consts import combinedOptions


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
    if (selectedOptionIdx < 0) or (selectedOptionIdx > 11):
        print("Error during passing 'selectedOptionIdx' argument, it has to be in range of <0,11>")
        sys.exit(1)

    # --Load image paths (list of dictionaries)--
    print(f"1. Getting images paths ...")
    loadedImagePaths = loadImagePaths(inputImagesFolderPath)

    # --Performing recognitions--
    print(f"2. Performing recognitions ...")

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

    # --Calc accuracy and other params of results--
    print(f"3. Calculating accuracy and other params ...")
    calcedAcc, numOfErrorTerminations, numOfProperRecognitions = calcAccuracy(recognitionResults)

    # --Save results to files--
    print(f"4. Saving results to output file ...")
    saveResultsToFile(recognitionResults,
                      calcedAcc,
                      numOfErrorTerminations,
                      numOfProperRecognitions,
                      combinedOptions[selectedOptionIdx])
    # TODO - e.g. confusion matrix (for each letter - row predict, col real), save accuracy to file


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF 'main-test.py' SCRIPT --")
