# Standard imports
import sys
from os.path import isfile, dirname, join

# Custom functions imports
sys.path.append(join(dirname(__file__), "functions"))  # important - it not used, "rescaleSkeleton" module is not found

from functions.getArgumentOptionsSingle import getArgumentOptionsSingle
from functions.skeletons.MediaPipe.getMediaPipeSk import getMediaPipeSk
from functions.skeletons.OpenPose.getOpenPoseSk import getOpenPoseSk
from functions.resizeImage import resizeImage
from functions.rescaleSkeleton import rescaleSkeleton


def main(argv):
    # --Consts--
    desiredImageWidth: int = 640  # in pixels
    desiredImageHeight: int = 480  # in pixels

    # --Option variables--
    useMediaPipe: bool = True  # default: True
    useMatlabPreprocessing: bool = True  # default: True
    useShiftedData: bool = True  # default: True
    inputFolderPath: str = ""  # default: ""
    inputImageName: str = "P2_A.bmp"  # default: "P2_A.bmp"
    useImageResize: bool = False  # default: False (use image rescale - True, or skeleton rescale, considered as better one - False)
    useCuda: bool = False  # default: False - it's faster for single evaluation to use CPU than GPU (moving data to GPU - CUDA costs more than evaluation benefits gained from it)

    # --Read input arguments and set variables--
    useMediaPipe, useMatlabPreprocessing, useShiftedData, inputFolderPath, inputImageName, useImageResize, useCuda = getArgumentOptionsSingle(argv,
                                                                                                                                              useMediaPipe,
                                                                                                                                              useMatlabPreprocessing,
                                                                                                                                              useShiftedData,
                                                                                                                                              inputFolderPath,
                                                                                                                                              inputImageName,
                                                                                                                                              useImageResize,
                                                                                                                                              useCuda)
    # Specify "inputImageFilePath"
    if inputFolderPath != "":
        inputImageFilePath = join(inputFolderPath, inputImageName)
    else:
        inputImageFilePath = join(dirname(__file__), "input", inputImageName)

    # -- Check whether input file exists --
    if not isfile(inputImageFilePath):
        raise Exception("Input file doesn't exist in input folder.")

    # -- Change input image size (perform resize) - if "useImageRescale" is True --
    if useImageResize:
        print(f"0. Change input image size ...")
        splittedInputImageFileName = inputImageName.split(".")
        newInputImageName = splittedInputImageFileName[0] + "_res" + "." + splittedInputImageFileName[1]

        if inputFolderPath != "":
            outputImageFilePath = join(inputFolderPath, newInputImageName)
        else:
            outputImageFilePath = join(dirname(__file__), "input", "resized", newInputImageName)

        if (resizeImage(inputImageFilePath,
                        outputImageFilePath,
                        desiredImageWidth,
                        desiredImageHeight)):
            # Set input image file path name to resized one - when resize was performed
            inputImageFilePath = outputImageFilePath  # it's not error here, that we use "outputImageFilePath"

    # --Get skeleton using either MediaPipe or OpenPose (based on selected method)
    if useMediaPipe:
        print(f"1. Getting skeleton using MediaPipe ...")
        outputTxtFilePath = getMediaPipeSk(inputImageFilePath)
    else:
        print(f"1. Getting skeleton using OpenPose ...")  # old: inputImageName
        outputTxtFilePath = getOpenPoseSk(inputImageFilePath)  # old: inputImageName

    print(f"outputTxtFilePath: {outputTxtFilePath}")

    # -- Rescale output skeleton, if "useImageRescale" is False --
    if not useImageResize:
        print(f"1.5. Rescale output skeleton ...")
        rescaleSkeleton(inputImageFilePath,
                        outputTxtFilePath,
                        desiredImageWidth,
                        desiredImageHeight)

    # --Run Matlab preprocessing (skeleton transformation script) - if "useMatlabPreprocessing" is True--
    if useMatlabPreprocessing:
        # TODO
        pass


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF SCRIPT --")
