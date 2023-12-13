import sys
from os.path import dirname, join, exists
import torch
from torchmetrics import ConfusionMatrix
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt

from functions.getArgumentOptionsBatch import getArgumentOptionsBatch
from functions.getLettersFromListStr import getLettersFromListStr
from functions.reduceBlankRecognitions import reduceBlankRecognitions
from functions.mapRecognitionsToIndexes import mapRecognitionsToIndexes
from exceptions.ErrorInputFileLetter import ErrorInputFileLetter
from exceptions.ErrorMismatchResultLen import ErrorMismatchResultLen

sys.path.append(dirname(dirname(__file__)))
from consts.consts import availableLetters


def showConfusionMatrix(pathToInputFile: str):
    with open(pathToInputFile, "r") as f:
        fileContent = f.read()
        splittedFileContent = fileContent.split("\n")

        if len(splittedFileContent) > 3:
            predictedResultsStr = splittedFileContent[2]
            realResultsStr = splittedFileContent[3]

            try:
                # --Transforming str into list--
                predictedResults = getLettersFromListStr(predictedResultsStr)
                realResults = getLettersFromListStr(realResultsStr)

                # --Reducing both predicted and real lists with corresponding blank elements (blank element is "-")--
                predictedResults, realResults = reduceBlankRecognitions(predictedResults, realResults)

                # --Map results in str to it's corresponding indexes--
                predictedResultsIdx = mapRecognitionsToIndexes(predictedResults)
                realResultsIdx = mapRecognitionsToIndexes(realResults)

                # --Plot confusion matrix--
                # Transform list into torch tensors
                predictedResultsIdxTensor = torch.tensor(predictedResultsIdx)
                realResultsIdxTensor = torch.tensor(realResultsIdx)

                # Setup confusion instance and compare predictions to targets
                confmat = ConfusionMatrix(num_classes=len(availableLetters),
                                          task="multiclass")

                # Plot confusion matrix
                confmatTensor = confmat(preds=predictedResultsIdxTensor,
                                        target=realResultsIdxTensor)

                # Plot the confusion matrix
                fig, ax = plot_confusion_matrix(
                    conf_mat=confmatTensor.numpy(),  # matplotlib likes working with numpy
                    class_names=availableLetters,
                    show_absolute=False,
                    show_normed=True,
                    figsize=(11, 9)
                )

                plt.title(f"Confusion matrix. Options: {splittedFileContent[1].split(': ')[1]}")
                plt.show()

            except (ErrorInputFileLetter, ErrorMismatchResultLen, ValueError) as e:
                print(f"{e} Terminating script.")
                sys.exit(1)
        else:
            print("Wrong input file format. Terminating script.")
            sys.exit(1)


if __name__ == "__main__":
    # --Option variables--
    resultFileName = "results_1.txt"  # default "results_1.txt"

    # --Read input arguments and set variables--
    resultFileName = getArgumentOptionsBatch(sys.argv[1:],
                                             resultFileName)

    # --Check whether result file exists--
    print(f"1. Checking existence of result file ...")
    pathToInputFile = join(dirname(dirname(__file__)), "output", resultFileName)  # .replace("\\", "\\\\")  replace one slash with 2 slashes

    if not exists(pathToInputFile):
        print(f"File named \"{resultFileName}\" doesn't exist. Terminating batch script.")
        sys.exit(1)

    # --Preparing confusion matrix to show--
    print(f"1. Preparing confusion matrix to show ...")
    showConfusionMatrix(pathToInputFile)

    print("-- END OF 'batch-showConfusionMatrix.py' SCRIPT --")
