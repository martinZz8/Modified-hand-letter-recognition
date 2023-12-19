# Standard imports
import sys
from os.path import dirname, join
import shutil
import subprocess

sys.path.append(dirname(dirname(__file__)))
sys.path.append(dirname(__file__))
from skeletons.OpenPose.checkIfOutputIsProper import checkIfOutputIsProper
from fileRemoveRowsInSkeleton import fileRemoveRowsInSkeleton


def getMatlabPreprocessedSkeleton(outputTxtFilePath: str,
                                  useMediaPipe: bool,
                                  useShiftedData: bool):
    # If "useMediaPipe"=False, check whether input skeleton has more than 22 elements - if so, remove extra elements
    doRemoveLastRowInMatlabScript = False

    if not useMediaPipe:
        resBool, numOfLandmarks = checkIfOutputIsProper(outputTxtFilePath)

        if numOfLandmarks > 22:
            fileRemoveRowsInSkeleton(outputTxtFilePath, True, 22)

        # Here we compare old number, reduced to 22 if before was greater than 22
        if numOfLandmarks >= 22:
            doRemoveLastRowInMatlabScript = True
    # print(f"doRemoveLastRowInMatlabScript: {doRemoveLastRowInMatlabScript}")

    # Determine "matlabPreprocessorCwd"
    matlabPreprocessorCwd = dirname(__file__)

    for i in range(4):
        matlabPreprocessorCwd = dirname(matlabPreprocessorCwd)

    matlabPreprocessorCwd = join(matlabPreprocessorCwd, "Matlab-single-classifier")

    # Determine "inputFileName"
    splittedOutputTxtFilePath = outputTxtFilePath.split("\\")
    inputFileName = splittedOutputTxtFilePath[len(splittedOutputTxtFilePath) - 1]

    # Copy input file into "input" folder located in cwd of Matlab's script
    pathToMatlabPreprocessorInputDirectoryFilePath = join(matlabPreprocessorCwd, "input", inputFileName)
    shutil.copyfile(outputTxtFilePath, pathToMatlabPreprocessorInputDirectoryFilePath)

    # Determine arguments for script "main.m"
    scriptProgramName = "matlab"
    scriptRunMode = "-batch"
    scriptAddParameters = f"\"inputFileName='{inputFileName}';" \
                          f" useMediaPipe='{'true' if useMediaPipe else 'false'}';" \
                          f" useShiftedOut='{'true' if useShiftedData else 'false'}';" \
                          f" deleteLastRow='{'true' if doRemoveLastRowInMatlabScript else 'false'}';" \
                          f" run('main.m'); exit;\""

    # Run Matlab's preprocessing script
    ls_output = subprocess.Popen([scriptProgramName, scriptRunMode, scriptAddParameters], cwd=matlabPreprocessorCwd)
    ls_output.communicate()  # Will block for 30 seconds

    # Determine output file name
    matlabPreprocessorOutputFilePath = join(matlabPreprocessorCwd, "output", "TransformedSkeleton.txt")

    return matlabPreprocessorOutputFilePath
