# Standard imports
import sys
from os.path import isfile, dirname, join

# Custom functions imports
from functions.getArgumentOptionsSingle import getArgumentOptionsSingle
from functions.skeletons.MediaPipe.getMediaPipeSk import getMediaPipeSk
from functions.skeletons.OpenPose.getOpenPoseSk import getOpenPoseSk


def main(argv):
    # --Consts--
    inputFolderName: str = "input"
    outputFolderName: str = "output"
    desiredImageWidth: int = 640  # in pixels
    desiredImageHeight: int = 480  # in pixels

    # --Option variables--
    useMediaPipe: bool = True  # default: True
    useShiftedData: bool = True  # default: True
    inputImageName: str = "P2_A.bmp"  # default: "P2_A.bmp"
    useImageRescale: bool = False  # default: False (use image rescale - True, or skeleton rescale, considered as better one - False)
    useCuda: bool = False  # default: False - it's faster for single evaluation to use CPU than GPU (moving data to GPU - CUDA costs more than evaluation benefits gained from it)

    # --Read input arguments and set variables--
    useMediaPipe, useShiftedData, inputImageName, useImageRescale, useCuda = getArgumentOptionsSingle(argv,
                                                                                                      useMediaPipe,
                                                                                                      useShiftedData,
                                                                                                      inputImageName,
                                                                                                      useImageRescale,
                                                                                                      useCuda)
    # -- Check whether input file exists --
    pathToFile = join(dirname(__file__), "input", inputImageName)
    if not isfile(pathToFile):
        raise Exception("Input file doesn't exist in input folder.")

    # -- Change input image size, if useImageRescale is True --
    if useImageRescale:
        # TODO
        pass

    # --Get skeleton using either MediaPipe or OpenPose (based on selected method)
    if useMediaPipe:
        outputTxtFilePath = getMediaPipeSk(inputImageName)
    else:
        outputTxtFilePath = getOpenPoseSk(inputImageName)

    print(f"outputTxtFilePath: {outputTxtFilePath}")

    # -- Rescale output skeletons, if useImageRescale is False --
    if not useImageRescale:
        # TODO
        pass


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF SCRIPT --")
