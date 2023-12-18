# Standard imports
import sys
from os.path import isfile, dirname, join, exists
from os import mkdir

# Custom functions imports
sys.path.append(join(dirname(__file__), "functions"))  # important - if not used, "rescaleSkeleton" module is not found

from functions.getArgumentOptionsSingle import getArgumentOptionsSingle
from functions.skeletons.MediaPipe.getMediaPipeSk import getMediaPipeSk
from functions.skeletons.OpenPose.getOpenPoseSk import getOpenPoseSk
from functions.resizeImage import resizeImage
from functions.rescaleSkeleton import rescaleSkeleton
from functions.preprocessing.getMatlabPreprocessedSkeleton import getMatlabPreprocessedSkeleton
from functions.preprocessing.locallyShiftSkeleton import locallyShiftSkeleton
from functions.preprocessing.fileRemoveLastRowInSkeleton import fileRemoveRowsInSkeleton
from functions.classify.getPyTorchClassification import getPyTorchClassification
from functions.classify.copyAndGetResultsOfClassify import copyAndGetResultsOfClassify
from functions.skeletons.exceptions.ErrorInputFileExtension import ErrorInputFileExtension
from functions.skeletons.exceptions.ErrorLandmarkDetection import ErrorLandmarkDetection


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
    outputFileName: str = "results.txt"  # default: "results.txt"
    useImageResize: bool = False  # default: False (use image rescale - True, or skeleton rescale, considered as slightly better one - False)
    useCuda: bool = False  # default: False - it's faster for single evaluation to use CPU than GPU (moving data to GPU - CUDA costs more than evaluation benefits gained from it)

    # --Read input arguments and set variables--
    useMediaPipe, useMatlabPreprocessing, useShiftedData, inputFolderPath, inputImageName, outputFileName, useImageResize, useCuda = getArgumentOptionsSingle(argv,
                                                                                                                                                              useMediaPipe,
                                                                                                                                                              useMatlabPreprocessing,
                                                                                                                                                              useShiftedData,
                                                                                                                                                              inputFolderPath,
                                                                                                                                                              inputImageName,
                                                                                                                                                              outputFileName,
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
    # Note!: Resized image is placed in folder "input/resized" and has suffix "_res.<ext>" (<ext> stands for extension)
    if useImageResize:
        print(f"0. Change input image size ...")
        splittedInputImageFileName = inputImageName.split(".")
        newInputImageName = splittedInputImageFileName[0] + "_res" + "." + splittedInputImageFileName[1]

        if inputFolderPath != "":
            resizedFolderPath = join(inputFolderPath, "resized")

            if not exists(resizedFolderPath):
                mkdir(resizedFolderPath)

            outputImageFilePath = join(resizedFolderPath, newInputImageName)
        else:
            outputImageFilePath = join(dirname(__file__), "input", "resized", newInputImageName)

        if (resizeImage(inputImageFilePath,
                        outputImageFilePath,
                        desiredImageWidth,
                        desiredImageHeight)):
            # Set input image file path name to resized one - when resize was performed
            inputImageFilePath = outputImageFilePath  # it's not error here, that we use "outputImageFilePath"

    # --Get skeleton using either MediaPipe or OpenPose (based on selected method)
    # Note!: If image was resized before (useImageResize=True), skeleton provided in "outputTemp" folder of either OpenPose or MediaPipe libraries has "_res.txt" suffix.
    try:
        if useMediaPipe:
            print(f"1. Getting skeleton using MediaPipe ...")
            outputTxtFilePath = getMediaPipeSk(inputImageFilePath)
        else:
            print(f"1. Getting skeleton using OpenPose ...")  # old: inputImageName
            outputTxtFilePath = getOpenPoseSk(inputImageFilePath)  # old: inputImageName
    except (ErrorInputFileExtension, ErrorLandmarkDetection) as e:
        print(f"Error during determining {'MediaPipe' if useMediaPipe else 'OpenPose'}'s skeleton. Terminating program abnormally.")
        sys.exit(1)  # Note! return codes can only have natural values (with zero included, which indicates proper execution of script - other ones are errors)

    print(f"outputTxtFilePath: {outputTxtFilePath}")

    # -- Rescale output skeleton, if "useImageRescale" is False --
    if not useImageResize:
        print(f"1.5. Rescale output skeleton ...")
        rescaleSkeleton(inputImageFilePath,
                        outputTxtFilePath,
                        desiredImageWidth,
                        desiredImageHeight)

    # --Run "Matlab-single-classifier" preprocessing (skeleton transformation script) - if "useMatlabPreprocessing" is True--
    skeletonFromCopyPath = outputTxtFilePath
    if useMatlabPreprocessing:
        print(f"1.6. Performing Matlab skeleton preprocessing ...")
        skeletonFromCopyPath = getMatlabPreprocessedSkeleton(outputTxtFilePath,
                                                             useMediaPipe,
                                                             useShiftedData)
    elif useShiftedData:
        # If Matlab preprocessing is disabled, but we want to shift our data, we can perform it using our Python's method
        print(f"1.6. Performing local skeleton shift ...")
        locallyShiftSkeleton(skeletonFromCopyPath, useMediaPipe)
    elif not useMediaPipe:
        # If "useMatlabPreprocessing=False" AND "useShiftedData=False", we have to remove last row from OpenPose skeleton data
        fileRemoveRowsInSkeleton(skeletonFromCopyPath, True)

    # --Run "Python-eval-model" script to classify skeleton by PyTorch's model--
    print(f"1.7. Getting PyTorch classification ...")
    outputClassifyFilePath = getPyTorchClassification(skeletonFromCopyPath,
                                                      outputFileName,
                                                      useMediaPipe,
                                                      useShiftedData,
                                                      useCuda)

    # -- Read results of classification by "Python-eval-model" script
    print(f"1.8. Copying results of classification and printing them out ...")
    resultsOfClassify = copyAndGetResultsOfClassify(outputClassifyFilePath)

    print(resultsOfClassify)


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF 'main-single.py' SCRIPT --")
