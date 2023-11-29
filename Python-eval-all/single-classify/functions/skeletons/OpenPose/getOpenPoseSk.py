# Standard imports
import sys
from os.path import dirname, join
import subprocess

sys.path.append(dirname(__file__))
from replaceCharactersInFile import replaceCharactersInFile


def hasFileNameProperExtension(inputFileName: str,
                               properFileExtensions: list[str]):
    isProper = False

    for fileExt in properFileExtensions:
        if fileExt in inputFileName:
            isProper = True
            break

    return isProper


def getOpenPoseSk(inputImageFilePath: str):
    # -- Determine if "inputFileName" has proper extension --
    splittedImageFilePath = inputImageFilePath.split("\\")
    inputFileName = splittedImageFilePath[len(splittedImageFilePath) - 1]
    can_continue = hasFileNameProperExtension(inputFileName, [".png", ".jpg", ".jpeg", ".bmp"])

    if not can_continue:
        raise Exception(
            "Input file doesn't have proper extension. Supported extensions: ['.png', '.jpg', '.jpeg', '.bmp']")

    # -- Constants definitions --
    openPoseExecName = "GetOpenPoseSkeleton.exe"
    outputFileNameFromExec = "skeletonData.txt"

    # -- Prepare file paths --
    splittedFileName = inputFileName.split(".")
    fileNameWoExt = ".".join(splittedFileName[0:(len(splittedFileName) - 1)])
    inputFilePath = inputImageFilePath  # "../../../input/"+inputFileName
    outputFilePath = "outputTemp/" + fileNameWoExt + ".txt"

    # -- Run OpenPose exec --
    # Note!
    # 1. It's important to set relative path to our exec to run "subprocess.Popen()" method properly
    # 2. You have also to sed "cwd" parameter in this method, since program will not find required dll and other model files
    pathToExec = join(dirname(__file__), "GetOpenPoseSkeleton.exe")
    cwd = dirname(__file__)

    ls_output = subprocess.Popen([pathToExec, inputFilePath, outputFilePath], cwd=cwd)
    ls_output.communicate()  # Will block for 30 seconds

    # -- Replace in saved skeleton "\t" with " " (tab with space) --
    # Since "GetOpenPoseSkeleton.exe" file uses "\t" as delimiter
    pathToOutputFile = join(dirname(__file__), "outputTemp", fileNameWoExt + ".txt")
    replaceCharactersInFile(pathToOutputFile, "\t", " ", True)

    print("End of 'getOpenPoseSk.py' function")

    return join(cwd, "outputTemp", fileNameWoExt + ".txt")
