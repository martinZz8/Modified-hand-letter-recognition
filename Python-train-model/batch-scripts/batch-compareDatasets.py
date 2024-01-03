import sys
from os.path import dirname, join

from getBatchCompareArgumentOptions import getBatchCompareArgumentOptions
from functions.compareTwoDatasets import compareTwoDatasets

sys.path.append(join(dirname(dirname(dirname(__file__))), "Python-eval-model", "functions"))
from saveEvalResultsToFile import saveEvalResultsToFile


def main(argv):
    # --Consts--
    pathToDatasetsFolder = join(dirname(dirname(__file__)), "datasets")
    pathToNormalDatasetFolder = join(pathToDatasetsFolder, "normal")
    pathToShiftedDatasetFolder = join(pathToDatasetsFolder, "shifted")

    # --Option variables--
    useMediaPipe: bool = False
    useShiftedDataset: bool = False
    firstDatasetVersion: int = 1
    secondDatasetVersion: int = 2
    outputFileName: str = ""

    # --Read input arguments and set variables--
    useMediaPipe, useShiftedDataset, firstDatasetVersion, secondDatasetVersion, outputFileName = getBatchCompareArgumentOptions(argv,
                                                                                                                                useMediaPipe,
                                                                                                                                useShiftedDataset,
                                                                                                                                firstDatasetVersion,
                                                                                                                                secondDatasetVersion,
                                                                                                                                outputFileName)

    # --Check whether first and second dataset version are different--
    if firstDatasetVersion == secondDatasetVersion:
        raise Exception(f"Error: given versions of datasets to compare are same and equal: {firstDatasetVersion}")

    # --Determine used dataset--
    # Check if we use shifted dataset
    if useShiftedDataset:
        pathToFirstComparedDataset = pathToShiftedDatasetFolder
        pathToSecondComparedDataset = pathToShiftedDatasetFolder
    else:
        pathToFirstComparedDataset = pathToNormalDatasetFolder
        pathToSecondComparedDataset = pathToNormalDatasetFolder

    # Check if we use MediaPipe
    if useMediaPipe:
        pathToFirstComparedDataset = join(pathToFirstComparedDataset, "MediaPipe")
        pathToSecondComparedDataset = join(pathToSecondComparedDataset, "MediaPipe")
    else:
        pathToFirstComparedDataset = join(pathToFirstComparedDataset, "OpenPose")
        pathToSecondComparedDataset = join(pathToSecondComparedDataset, "OpenPose")

    # Check for version of dataset
    if firstDatasetVersion != 1:
        pathToFirstComparedDataset += str(firstDatasetVersion)

    if secondDatasetVersion != 1:
        pathToSecondComparedDataset += str(secondDatasetVersion)

    #print(f"pathToFirstComparedDataset: {pathToFirstComparedDataset}")
    #print(f"pathToSecondComparedDataset: {pathToSecondComparedDataset}")

    # --Compare first and second dataset--
    resultStr = compareTwoDatasets(pathToFirstComparedDataset,
                                   pathToSecondComparedDataset)

    # --Save results to file--
    pathToOutputDir = join(dirname(__file__), "output")
    saveEvalResultsToFile(pathToOutputDir, outputFileName, resultStr)


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF SCRIPT --")
