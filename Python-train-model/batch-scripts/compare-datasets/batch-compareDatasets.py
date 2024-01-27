import sys
from os.path import dirname, join

from getBatchCompareArgumentOptions import getBatchCompareArgumentOptions
from functions.compareTwoDatasets import compareTwoDatasets
from functions.joinPathsToDatasets import joinPathsToDatasets

sys.path.append(join(dirname(dirname(dirname(dirname(__file__)))), "Python-eval-model", "functions"))
from saveEvalResultsToFile import saveEvalResultsToFile


def main(argv):
    # --Consts--
    pathToDatasetsFolder = join(dirname(dirname(dirname(__file__))), "datasets")

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
    pathToFirstComparedDataset, pathToSecondComparedDataset = joinPathsToDatasets(pathToDatasetsFolder,
                                                                                  useShiftedDataset,
                                                                                  useMediaPipe,
                                                                                  firstDatasetVersion,
                                                                                  secondDatasetVersion)

    # --Compare first and second dataset--
    resultStr = compareTwoDatasets(pathToFirstComparedDataset,
                                   pathToSecondComparedDataset)

    # --Save results to file--
    pathToOutputDir = join(dirname(__file__), "output")
    outputFileName = saveEvalResultsToFile(pathToOutputDir, outputFileName, resultStr)

    print(f"Output file name (placed in \"output\" folder): {outputFileName}")

if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF SCRIPT --")
