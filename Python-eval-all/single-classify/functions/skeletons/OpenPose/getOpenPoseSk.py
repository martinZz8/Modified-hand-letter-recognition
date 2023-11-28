# Standard imports
from os.path import dirname, join
import subprocess


def hasFileNameProperExtension(inputFileName: str,
                               properFileExtensions: list[str]):
    isProper = False

    for fileExt in properFileExtensions:
        if fileExt in inputFileName:
            isProper = True
            break

    return isProper


def getOpenPoseSk(inputFileName: str):
    # -- Determine if "inputFileName" has proper extension --
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
    inputFilePath = "../../../input/"+inputFileName
    outputFilePath = "outputTemp/" + fileNameWoExt + ".txt"

    # -- Run OpenPose exec --
    # Note!
    # 1. It's important to set relative path to our exec to run "subprocess.Popen()" method properly
    # 2. You have also to sed "cwd" parameter in this method, since program will not find required dll and other model files
    pathToExec = join(dirname(__file__), "GetOpenPoseSkeleton.exe")
    cwd = dirname(__file__)

    ls_output = subprocess.Popen([pathToExec, inputFilePath, outputFilePath], cwd=cwd)
    ls_output.communicate()  # Will block for 30 seconds

    print("End of 'getOpenPoseSk.py' function")

    return join(cwd, "outputTemp", fileNameWoExt + ".txt")
