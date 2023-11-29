from os.path import dirname, join
import shutil
import subprocess


def getPyTorchClassification(inputSkeletonPath: str,
                             outputFileName: str,
                             useMediaPipe: bool,
                             useShiftedData: bool,
                             useCuda: bool):
    # Get output file name from "outputSkeletonPath"
    splittedInputSkeletonPath = inputSkeletonPath.split("\\")
    inputFileName = splittedInputSkeletonPath[len(splittedInputSkeletonPath)-1]

    # Determine "classifySkeletonCwd"
    classifySkeletonCwd = dirname(__file__)

    for i in range(4):
        classifySkeletonCwd = dirname(classifySkeletonCwd)

    classifySkeletonCwd = join(classifySkeletonCwd, "Python-eval-model")

    # Determine "skeletonToCopyPath"
    skeletonToCopyPath = join(classifySkeletonCwd, "input", inputFileName)

    # Copy file from "outputSkeletonPath" to "skeletonToCopyPath"
    shutil.copyfile(inputSkeletonPath, skeletonToCopyPath)

    # Determine arguments for script "main-eval.py"
    scriptProgramName = "py"
    scriptPythonVersion = "-3"
    scriptName = "main-eval.py"
    scriptAddParameters = [
        '-m' if useMediaPipe else '-o',
        '-s' if useShiftedData else '-S',
        '-c' if useCuda else '-C',
        '-i',
        inputFileName,
        '-u',
        outputFileName
    ]

    # Run Python classifier script
    # Also note, how to throw stdout from subprocess away: https://stackoverflow.com/questions/7082623/suppress-output-from-subprocess-popen
    ls_output = subprocess.Popen([scriptProgramName, scriptPythonVersion, scriptName] + scriptAddParameters, cwd=classifySkeletonCwd)
    ls_output.communicate()  # Will block for 30 seconds

    # Specify output classify file path
    outputClassifyFilePath = join(classifySkeletonCwd, "output", outputFileName)

    return outputClassifyFilePath
