from os.path import dirname, join
import shutil


def copyAndGetResultsOfClassify(outputClassifyFilePath: str):
    # Read file placed in "outputClassifyFilePath"
    with open(outputClassifyFilePath, "r") as file:
        fileContent = file.read()

    # Copy file to "output" folder of "single-classify" script
    splittedOutputClassifyFilePath = outputClassifyFilePath.split("\\")
    outputClassifyFileName = splittedOutputClassifyFilePath[len(splittedOutputClassifyFilePath)-1]

    outputToCopyPath = join(dirname(dirname(dirname(__file__))), "output", outputClassifyFileName)

    shutil.copyfile(outputClassifyFilePath, outputToCopyPath)

    return fileContent
